from django.urls import path
from .views import CustomUserListView
from .auth_views import LoginView, RefreshView, LogoutView, MeView,RegisterView

urlpatterns = [
    path("", CustomUserListView.as_view(), name="accounts"),
    path("login/", LoginView.as_view()),
    path("refresh/", RefreshView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("me/", MeView.as_view()),
    path("register/", RegisterView.as_view()),
]
