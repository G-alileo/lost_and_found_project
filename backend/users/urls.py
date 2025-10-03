from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import AdminSessionLoginView, MeView, RegisterView, ChangePasswordView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/admin-login/", AdminSessionLoginView.as_view(), name="admin-login"),
    path("users/me/", MeView.as_view(), name="users-me"),
    path("users/change-password/", ChangePasswordView.as_view(), name="change-password"),
]


