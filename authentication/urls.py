from django.urls import path

from authentication.views import (
    AuthLoginView,
    AuthLogoutView,
    AuthResetPasswordGetEmailView,
    AuthResetPasswordResetView,
    AuthResetPasswordSetTokenView,
)

app_name = "auth"

urlpatterns = [
    path("login/", AuthLoginView.as_view(), name="login-view"),
    path(
        "reset-password/email",
        AuthResetPasswordGetEmailView.as_view(),
        name="password-reset-get-email",
    ),
    path(
        "reset-password/token",
        AuthResetPasswordSetTokenView.as_view(),
        name="password-reset-set-token",
    ),
    path(
        "reset-password/password",
        AuthResetPasswordResetView.as_view(),
        name="password-reset",
    ),
    path("logout/", AuthLogoutView.as_view(), name="logout-view"),
]
