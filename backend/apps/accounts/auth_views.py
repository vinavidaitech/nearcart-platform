from datetime import timedelta
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer

from django.core.cache import cache
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.throttling import AnonRateThrottle
import random
from .serializers import RegisterRequestSerializer, VerifyOTPSerializer
from .models import CustomUser



def _set_refresh_cookie(response, refresh_token):
    response.set_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        value=str(refresh_token),
        max_age=int(timedelta(days=7).total_seconds()),
        httponly=True,
        secure=settings.REFRESH_COOKIE_SECURE,
        samesite=settings.REFRESH_COOKIE_SAMESITE,
        path="/api/auth/",  # only sent to auth endpoints
    )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response = Response({
            "access": str(access),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
            },
        })
        _set_refresh_cookie(response, refresh)
        return response


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        response = Response(
            {
                "access": str(access),
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role,
                },
            },
            status=status.HTTP_201_CREATED,
        )
        _set_refresh_cookie(response, refresh)
        return response


class RefreshView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        raw_token = request.COOKIES.get(settings.REFRESH_COOKIE_NAME)
        if not raw_token:
            return Response({"detail": "No refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken(raw_token)
            access = refresh.access_token
        except TokenError:
            return Response({"detail": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"access": str(access)})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        raw_token = request.COOKIES.get(settings.REFRESH_COOKIE_NAME)
        if raw_token:
            try:
                RefreshToken(raw_token).blacklist()
            except TokenError:
                pass
        response = Response({"detail": "Logged out"})
        response.delete_cookie(settings.REFRESH_COOKIE_NAME, path="/api/auth/")
        return response


class MeView(APIView):
    def get(self, request):
        u = request.user
        return Response({
            "id": str(u.id),
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "is_verified": u.is_verified,
        })



OTP_TTL_SECONDS = 10 * 60
MAX_OTP_ATTEMPTS = 5

def _otp_cache_key(email):
    return f"register_otp:{email.lower().strip()}"

class OTPRequestThrottle(AnonRateThrottle):
    scope = "otp_request"
    rate = "3/min"

class RequestRegisterOTPView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [OTPRequestThrottle]

    def post(self, request):
        serializer = RegisterRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        email = data["email"].lower().strip()

        code = f"{random.randint(0, 999999):06d}"
        cache.set(_otp_cache_key(email), {
            "full_name": data["full_name"],
            "password_hash": make_password(data["password"]),
            "otp_hash": make_password(code),
            "attempts": 0,
        }, timeout=OTP_TTL_SECONDS)

        send_mail(
            subject="Your NearCart verification code",
            message=f"Your verification code is {code}. It expires in 10 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        return Response({"detail": "OTP sent to email."}, status=200)


class VerifyRegisterOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].lower().strip()
        code = serializer.validated_data["otp"]

        key = _otp_cache_key(email)
        pending = cache.get(key)
        if not pending:
            return Response({"detail": "No pending verification, or it expired. Please request a new OTP."}, status=400)

        if pending["attempts"] >= MAX_OTP_ATTEMPTS:
            cache.delete(key)
            return Response({"detail": "Too many attempts. Please request a new OTP."}, status=400)

        if not check_password(code, pending["otp_hash"]):
            pending["attempts"] += 1
            cache.set(key, pending, timeout=OTP_TTL_SECONDS)
            return Response({"detail": "Incorrect OTP."}, status=400)

        if CustomUser.objects.filter(email=email).exists():
            cache.delete(key)
            return Response({"detail": "An account with this email already exists."}, status=400)

        user = CustomUser(
            email=email,
            full_name=pending["full_name"],
            role=CustomUser.Role.OWNER,
            is_verified=True,
        )
        user.password = pending["password_hash"]
        user.save()
        cache.delete(key)

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        response = Response({
            "access": str(access),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
            },
        }, status=201)
        _set_refresh_cookie(response, refresh)
        return response
