from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import CustomUser


# apps/accounts/serializers.py
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id", "email", "phone", "full_name", "role",
            "is_verified", "avatar_url", "preferred_radius_km",
            "created_at",
        ]
        read_only_fields = ["id", "email", "role", "is_verified", "created_at"]



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ["email", "full_name", "password"]

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            full_name=validated_data["full_name"],
            role=CustomUser.Role.OWNER,
        )

