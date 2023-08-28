from typing import Any

from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
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
            return JsonResponse({"Error": "User not found."}, status=404)

        if new_password == new_password_confirm and user.check_password(old_password):
            try:
                if validate_password(new_password):
                    user.set_password(new_password)
                    user.save()
                    return JsonResponse({"Message": "Password successfully changed."})
            except ValidationError as e:
                return JsonResponse({"Error": list(e.messages)}, status=400)
            return JsonResponse
        return JsonResponse({"Error": "Invalid input."}, status=400)


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
        try:
            user = User.objects.get(id=request.user.id)
            user.delete()
        except Exception:
            return redirect("auth:login-view")    
        return redirect("auth:login-view")


class UserSettingsView(View, LoginRequiredMixin):
    template_name = "user/settings.html"
    page = "settings"
    title = "Settings"
    context = {
        "page": page,
        "title": title,
    }

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        user = User.objects.filter(id=request.user.id).first()
        if not user:
            return redirect("auth:login-view")

        return render(request, self.template_name, self.context)


class UserProfileView(View, LoginRequiredMixin):
    template_name = "user/profile.html"
    page = "profile"
    title = "Profile"
    context = {
        "page": page,
        "title": title,
    }

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        user = User.objects.filter(id=request.user.id).first()
        if not user:
            return redirect("auth:login-view")
        user_profile = Profile.objects.filter(user=request.user).first()
        if not user_profile:
            return redirect("user:edit-profile-view")

        self.context.update(
            {
                "user_profile": user_profile,
            }
        )
        return render(request, self.template_name, self.context)


class UserEditProfileView(View, LoginRequiredMixin):
    template_name = "user/update-profile.html"
    page = "profile"
    title = "Edit Profile"
    context = {
        "page": page,
        "title": title,
    }

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        user = User.objects.filter(id=request.user.id).first()
        if not user:
            return redirect("auth:login-view")
        user_profile_exists = Profile.objects.filter(user=request.user).exists()
        if user_profile_exists:
            user_profile = Profile.objects.get(user=request.user)

            self.context.update({"user_profile": user_profile})
            return render(request, self.template_name, self.context)

        return render(request, self.template_name, self.context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        user = User.objects.filter(id=request.user.id).first()
        if not user:
            return redirect("auth:login-view")

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        user_profile_exists = Profile.objects.filter(user=request.user).exists()
        if user_profile_exists:
            user_profile = Profile.objects.get(user=request.user)
            user_profile.first_name = first_name
            user_profile.last_name = last_name
            user_profile.email = email
            user_profile.phone = phone

            if "image" in request.FILES:
                user_profile.image = request.FILES["image"]

            user_profile.save()

            return redirect("user:profile-view")

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

        return redirect("user:profile-view")


class UserCreateView(View):
    template_name = "user/register.html"
    title = "Register"
    context = {"title": title}

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template_name, self.context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if User.objects.filter(email=email).exists():
            self.context.update(
                {
                    "error_message": [
                        "Invalid input. This email address is already \
                associated with an account."
                    ]
                }
            )
            return render(request, self.template_name, self.context, status=409)

        if password == confirm_password:
            if not User.objects.filter(email=email).exists():
                try:
                    validate_password(password)
                except ValidationError as e:
                    self.context.update({"error_message": list(e.messages)})
                    return render(request, self.template_name, self.context, status=400)
                User.objects.create_user(email, password)
                return redirect("auth:login-view")
        self.context.update(
            {
                "error_message": ["Invalid input. Passwords do not match"],
            }
        )
        return render(
            request,
            self.template_name,
            self.context,
            status=400,
        )
