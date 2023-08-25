from typing import Any

from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from pydantic import validate_email
from pydantic_core import PydanticCustomError

from user.models import Profile, User


class UserChangePasswordAction(View, LoginRequiredMixin):
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> JsonResponse:
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        new_password_confirm = request.POST.get("new_password_confirm")

        user = request.user
        if not user.is_authenticated:
            return JsonResponse({"Error": "User not found."})

        if new_password == new_password_confirm and user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return JsonResponse({"Message": "Password successfully changed."})
        return JsonResponse({"Error": "Invalid input."})


class UserChangeEmailAction(View, LoginRequiredMixin):
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> JsonResponse:
        try:
            new_email = request.POST.get("new_email")
            validate_email(new_email)
        except PydanticCustomError:
            return JsonResponse({"Error": "Invalid email address."}, status=400)

        if User.objects.filter(email=new_email).exists():
            return JsonResponse(
                {"Error": "An account is already associated with this email address."},
                status=400,
            )

        user = request.user
        user.email = new_email
        user.save()
        return JsonResponse({"Message": "User email was successfully changed."})

class UserDeleteAction(View, LoginRequiredMixin):
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        user = User.objects.filter(id=request.user.id).first()
        if user:
            user.delete()
        return redirect("auth:login-view")


class UserSettingsView(View, LoginRequiredMixin):
    template_name = "user/settings.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        user = User.objects.filter(id=request.user.id).first()
        if not user:
            return redirect("account:login-view")

        context = {
            "title": "Settings",
            "page": "settings",
        }
        return render(request, self.template_name, context)


class UserProfileView(View, LoginRequiredMixin):
    template_name = "user/profile.html"
    page = "profile"
    title = "Profile"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        user_profile = Profile.objects.filter(user=request.user).first()
        if not user_profile:
            return redirect("user:update-profile-view")

        context = {
            "user_profile": user_profile,
            "page": self.page,
            "title": self.title,
        }
        return render(request, self.template_name, context)


class UserEditProfileView(View, LoginRequiredMixin):
    template_name = "user/update-profile.html"
    page = "profile"
    title = "Edit Profile"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        user_profile, created = Profile.objects.get_or_create(user=request.user)

        context = {
            "user_profile": user_profile,
            "page": self.page,
            "title": self.title,
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        user_profile, created = Profile.objects.get_or_create(user=request.user)
        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.email = email
        user_profile.phone = phone

        if "image" in request.FILES:
            user_profile.image = request.FILES["image"]

        user_profile.save()

        return redirect("user:profile-view")


class UserCreateView(View):
    template_name = "user/register.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template_name)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            if not User.objects.filter(email=email).exists():
                User.objects.create_user(email, password)
                return redirect("auth:login-view")
        return render(
            request,
            self.template_name,
            {"error_message": "Invalid input.", "title": "Register"},
        )
