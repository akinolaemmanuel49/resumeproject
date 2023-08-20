from django.urls import path

from authentication.views import AuthLoginView, AuthLogoutView

app_name = "auth"

urlpatterns = [
    path("login/", AuthLoginView.as_view(), name="login-view"),
    path("logout/", AuthLogoutView.as_view(), name="logout-view"),
]
