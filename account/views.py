from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login

from account.models import Profile, User


# Create your views here.
class AccountDummyView(View):
    template_name = "account/dummy.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template_name)


class AccountSettingsView(View, LoginRequiredMixin):
    template_name = "account/settings.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return redirect("login-view")

        return render(request, self.template_name)


class AccountPasswordChangeView(View, LoginRequiredMixin):
    template_name = "account/password-change.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return redirect("login-view")

        return render(request, self.template_name)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        new_password_confirm = request.POST.get("new_password_confirm")

        if new_password == new_password_confirm:
            try:
                user: User = User.objects.get(id=request.user.id)
                if user.check_password(old_password):
                    user.set_password(new_password)
                else:
                    error_message = "Incorrect password."
                    return render(
                        request, self.template_name, {"error_message": error_message}
                    )
            except User.DoesNotExist:
                return redirect("login-view")
        else:
            error_message = "Passwords mismatch."
            return render(request, self.template_name, {"error_message": error_message})
        return redirect("profile-view")


class AccountProfileView(View, LoginRequiredMixin):
    template_name = "account/profile.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return redirect("update-profile-view")

        context = {"user_profile": user_profile, "page": "profile"}
        return render(request, self.template_name, context)


class AccountEditProfileView(View, LoginRequiredMixin):
    template_name = "account/update-profile.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user_profile = None

        context = {"user_profile": user_profile, "page": "profile"}
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        try:
            user_profile = Profile.objects.get(user=request.user)
            if user_profile:
                user_profile.first_name = first_name
                user_profile.last_name = last_name
                user_profile.email = email
                user_profile.phone = phone

        except Profile.DoesNotExist:
            user_profile = Profile.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                user=request.user,
            )

        if "image" in request.FILES:
            user_profile.image = request.FILES["image"]

        user_profile.save()

        return redirect("profile-view")


class AccountCreateView(View):
    template_name = "account/register.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template_name)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            try:
                user: User = User.objects.get(email=email)
                if user:
                    error_message = (
                        "An account is already associated with this email address."
                    )
                    return render(
                        request, self.template_name, {"error_message": error_message}
                    )
            except User.DoesNotExist:
                User.objects.create_user(email, password)
                return redirect("login-view")
        else:
            error_message = "Passwords mismatch."
            return render(request, self.template_name, {"error_message": error_message})
        return render(request, self.template_name)


class AccountLoginView(LoginView):
    template_name = "account/login.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template_name)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            try:
                profile = Profile.objects.get(user=user)
                if profile:
                    return redirect("profile-view")
            except Profile.DoesNotExist:
                return redirect("update-profile-view")
        else:
            error_message = "Invalid login credentials."
            return render(request, self.template_name, {"error_message": error_message})


class AccountLogoutView(LogoutView):
    next_page = reverse_lazy("dummy-view")
