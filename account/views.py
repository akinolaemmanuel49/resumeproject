from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser
from pydantic import EmailStr

from account.models import Profile, User
from resume.models import Resume


# Create your views here.
class AccountChangePasswordAction(View, LoginRequiredMixin):
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> JsonResponse:
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        new_password_confirm = request.POST.get("new_password_confirm")

        if new_password == new_password_confirm:
            user = request.user
            if isinstance(user, AnonymousUser):
                error_message = "User not found."
                response = {"Error": error_message}
                return JsonResponse(response)
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                response = {"Message": "Password successfully changed."}
                return JsonResponse(response)
            else:
                error_message = "Incorrect password."
                response = {"Error": error_message}
                return JsonResponse(response)


class AccountChangeEmailAction(View, LoginRequiredMixin):
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> JsonResponse:
        try:
            new_email: EmailStr = request.POST.get("new_email")
            print(new_email)
        except Exception as e:
            print(e)
            error_message = "Invalid email address."
            response = {"Error": error_message}
            return JsonResponse(response)
        if User.objects.filter(email=new_email).first():
            error_message = "An account is already associated with this email address."
            response = {"Error": error_message}
            return JsonResponse(response)
        else:
            user = request.user
            user.email = new_email
            user.save()
            message = "User email was successfully changed."
            response = {"Message": message}
            return JsonResponse(response)


class AccountHomeView(View):
    template_name = "account/dummy.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            print("DUMMY SIDE RESUME ID:", request.session["resume_id"])
        except Exception:
            print("DUMMY SIDE RESUME ID NOT SET")
        print("REMOTE IP ADDR: ", request.META["REMOTE_ADDR"])
        return render(request, self.template_name)


class AccountDummyView(View):
    template_name = "account/dummy.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            print("DUMMY SIDE RESUME ID:", request.session["resume_id"])
        except Exception:
            print("DUMMY SIDE RESUME ID NOT SET")
        print("REMOTE IP ADDR: ", request.META["REMOTE_ADDR"])
        return render(request, self.template_name)


class AccountDeleteAction(View, LoginRequiredMixin):
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            user: User = User.objects.get(id=request.user.id)
            user.delete()
        except User.DoesNotExist:
            return redirect("account:login-view")


class AccountSettingsView(View, LoginRequiredMixin):
    template_name = "account/settings.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return redirect("account:login-view")

        try:
            dashboard_user_resumes = (
                Resume.objects.filter(user=request.user)
                .order_by("-created_at")
                .all()[:3]
            )
        except Resume.DoesNotExist:
            context = {"title": "Settings", "page": "settings"}
            return render(request, self.template_name, context)

        context = {
            "title": "Settings",
            "page": "settings",
            "dashboard_user_resumes": dashboard_user_resumes,
        }
        return render(request, self.template_name, context)


class AccountProfileView(View, LoginRequiredMixin):
    template_name = "account/profile.html"
    page = "profile"
    title = "Profile"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return redirect("account:update-profile-view")

        try:
            dashboard_user_resumes = (
                Resume.objects.filter(user=request.user)
                .order_by("-created_at")
                .all()[:3]
            )
        except Resume.DoesNotExist:
            context = {"title": self.title, "page": self.page}
            return render(request, self.template_name, context)

        context = {
            "user_profile": user_profile,
            "page": self.page,
            "title": self.title,
            "dashboard_user_resumes": dashboard_user_resumes,
        }
        return render(request, self.template_name, context)


class AccountEditProfileView(View, LoginRequiredMixin):
    template_name = "account/update-profile.html"
    page = "profile"
    title = "Edit Profile"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            user_profile = None

        try:
            dashboard_user_resumes = (
                Resume.objects.filter(user=request.user)
                .order_by("-created_at")
                .all()[:3]
            )
        except Resume.DoesNotExist:
            context = {"title": self.title, "page": self.page}
            return render(request, self.template_name, context)

        context = {
            "user_profile": user_profile,
            "page": self.page,
            "title": self.title,
            "dashboard_user_resumes": dashboard_user_resumes,
        }
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

        return redirect("account:profile-view")


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
                    context = {"error_message": error_message, "title": "Register"}
                    return render(request, self.template_name, context)
            except User.DoesNotExist:
                User.objects.create_user(email, password)
                return redirect("account:login-view")
        else:
            error_message = "Passwords mismatch."
            context = {"error_message": error_message, "title": "Register"}
            return render(request, self.template_name, context)
        context = {"title": "Register"}
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
                    return redirect("account:profile-view")
            except Profile.DoesNotExist:
                return redirect("account:edit-profile-view")
        else:
            error_message = "Invalid login credentials."
            context = {"error_message": error_message, "title": "Login"}
            return render(request, self.template_name, context)


class AccountLogoutView(LogoutView):
    next_page = reverse_lazy("account:dummy-view")