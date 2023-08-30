from typing import Any

from django.http import HttpRequest, JsonResponse, HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ValidationError
from pydantic_core import PydanticCustomError
from resumeproject.utils import email_error_message_handler

from user.models import Profile, User
from resumeproject.utils import ProtectedView


# Create your views here.
class UserCreateView(View):
    template = "user/register.html"
    title = "Register"
    context = {"title": title}

    def add_message(self, request, message, level=messages.INFO):
        messages.add_message(request, level, message)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template, self.context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        # Get form data from request.
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Handle user already exists.
        if User.objects.filter(email=email).exists():
            self.context.update(
                {
                    "error_message": [
                        "Invalid input. This email address is already \
                associated with an account."
                    ]
                }
            )
            return render(request, self.template, self.context, status=409)

        # Handle password confirmation.
        if password == confirm_password:
            # Handle user creation.
            try:
                User.objects.create_user(email, password)
                # Pass message to template
                self.add_message(
                    request,
                    "You have successfully created an account. Please login.",
                    messages.SUCCESS,
                )
                return redirect("auth:login-view")
            # Handle errors arising from user creation.
            # Handle errors of the type ValidationError.
            except ValidationError as e:
                self.context.update({"error_message": list(e.messages)})
                return render(request, self.template, self.context, status=400)
            # Handle errors of the type PydanticCustomError.
            except PydanticCustomError as e:
                self.context.update(
                    {"error_message": email_error_message_handler(e.message())}
                )
                return render(request, self.template, self.context, status=400)
        else:
            self.context.update(
                {
                    "error_message": ["Invalid input. Passwords do not match"],
                }
            )
            return render(
                request,
                self.template,
                self.context,
                status=400,
            )


class UserEditProfileView(ProtectedView):
    template = "user/update-profile.html"
    page = "profile"
    title = "Edit Profile"
    context = {
        "page": page,
        "title": title,
    }
    next_page = "user:edit-profile-view"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            # Get the profile for the authenticated user.
            user_profile = Profile.objects.get(user=request.user)
            # Update context to include the user's profile instance.
            self.context.update({"user_profile": user_profile})
            return render(request, self.template, self.context)
        except Profile.DoesNotExist:
            return render(request, self.template, self.context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        # Get form data from request.
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        # Handle image data.
        if "image" in request.FILES:
            image = request.FILES["image"]
        else:
            image = None

        try:
            # Get profile for the authenticated user.
            user_profile = Profile.objects.get(user=request.user)
            # Update values if profile is found.
            user_profile.first_name = first_name
            user_profile.last_name = last_name
            user_profile.email = email
            user_profile.phone = phone
            user_profile.image = image
        # Handle Profile not found exception.
        except Profile.DoesNotExist:
            # Create a new profile instance if one does not exist.
            user_profile = Profile.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                user=request.user,
                image=image,
            )
        # Save the profile instance to the database.
        user_profile.save()
        # Redirect after the form is submitted.
        return redirect("user:profile-view")


class UserProfileView(ProtectedView):
    template = "user/profile.html"
    page = "profile"
    title = "Profile"
    context = {
        "page": page,
        "title": title,
    }
    next_page = "user:profile-view"

    def add_message(self, request, message, level=messages.INFO):
        messages.add_message(request, level, message)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            # Get the profile for the authenticated user.
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            # Redirect to edit-profile-view if profile does not exist.
            return redirect("user:edit-profile-view")

        # Update context to include the user's profile instance.
        self.context.update(
            {
                "user_profile": user_profile,
            }
        )
        return render(request, self.template, self.context)


class UserSettingsView(ProtectedView):
    template = "user/settings.html"
    page = "settings"
    title = "Settings"
    context = {
        "page": page,
        "title": title,
    }
    next_page = "user:settings-view"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template, self.context)


class UserDeleteAction(ProtectedView):
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return HttpResponse("DELETE")


class UserChangeEmailAction(ProtectedView):
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return HttpResponse("EMAIL")


class UserChangePasswordAction(ProtectedView):
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return HttpResponse("PASSWORD")


class DummyView(ProtectedView):
    next_page = "user:dummy-view"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return HttpResponse(content="Hell Yeah!")
