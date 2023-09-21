from typing import Any

from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from pydantic import validate_email
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

        if email:

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
        self.context.update(
            {
                "error_message": ["Invalid input. No email provided."],
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
        try:
            user = User.objects.get(id=request.user.id)
            user.delete()
            return redirect("home-view")
        except Exception:
            self.add_message(
                request, "An unexpected error has occurred.", messages.ERROR
            )
            return redirect("home-view")


class UserChangeEmailAction(ProtectedView):
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        new_email = request.POST.get("new_email")

        try:
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
        return JsonResponse(
            {"Message": "User email was successfully changed."}, status=200
        )


class UserChangePasswordAction(ProtectedView):
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> JsonResponse:
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        new_password_confirm = request.POST.get("new_password_confirm")

        user = request.user

        if new_password == new_password_confirm:
            try:
                if validate_password(new_password) is None:
                    if user.check_password(old_password):
                        user.set_password(new_password)
                        user.save()
                        return JsonResponse(
                            {"Message": "Password successfully changed."}, status=200
                        )
            except ValidationError as e:
                return JsonResponse({"Error": list(e.messages)}, status=400)
        else:
            return JsonResponse(
                {"Error": "Invalid input. Passwords do not match."}, status=400
            )
