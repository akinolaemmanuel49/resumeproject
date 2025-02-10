from typing import Any
from django.forms import ValidationError

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.views import View
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages

from user.models import Profile, Token, User
from resumeproject.utils import send_recover_password_mail


# Create your views here.
class AuthLoginView(LoginView):
    template = "auth/login.html"
    title = "Login"
    context = {
        "title": title,
    }

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template, self.context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            try:
                next_page = request.GET.get("next")
                if next_page:
                    return redirect(next_page)
                profile = Profile.objects.get(user=user)
                if profile:
                    return redirect("user:profile-view")
            except Profile.DoesNotExist:
                return redirect("user:edit-profile-view")
        else:
            error_message = "Invalid login credentials."
            self.context.update({"error_message": error_message})
            return render(request, self.template, self.context, status=401)


class AuthResetPasswordGetEmailView(View):
    template = "auth/password_reset_email.html"
    title = "Reset Password"
    context = {
        "title": title,
    }

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template, self.context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
            token = Token(user=user)
            _ = token.generate()
            token.save()
            try:
                user_profile = Profile.objects.get(user=user)
                send_recover_password_mail(
                    user_profile=user_profile,
                    recipient=user_profile.email,
                    variables={
                        "firstName":user_profile.first_name, 
                        "token": token.token, 
                        "support_email":"biteatertest@gmail.com", 
                        "company": "Biteater0"
                        }
                )
                return redirect("auth:password-reset-set-token")
            except Profile.DoesNotExist:
                send_recover_password_mail(
                    user_profile=user_profile,
                    recipient=user_profile.email,
                    variables={
                        "firstName":user_profile.first_name, 
                        "token": token.token, 
                        "support_email":"biteatertest@gmail.com", 
                        "company": "Biteater0"
                        }
                )
                return redirect("auth:password-reset-set-token")
        except User.DoesNotExist:
            self.context.update({"error_message": "User not found."})
            return render(request, self.template, self.context)


class AuthResetPasswordSetTokenView(View):
    template = "auth/password_reset_token.html"
    title = "Reset Password"
    context = {
        "title": title,
    }

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template, self.context)

    def post(
        self, request: HttpRequest, *args: str, **kwargs: Any
    ) -> HttpResponse | HttpResponseRedirect:
        token = request.POST.get("token")

        try:
            token = Token.objects.get(token=token, token_expires__gte=timezone.now())
            request.session["token_id"] = token.id
            return redirect("auth:password-reset")
        except Token.DoesNotExist:
            self.context.update({"error_message": "Invalid or expired token."})
            return render(request, self.template, self.context)


class AuthResetPasswordResetView(View):
    template = "auth/password_reset_password.html"
    title = "Reset Password"
    context = {
        "title": title,
    }

    def add_message(self, request: HttpRequest, message: str, level=messages.INFO):
        messages.add_message(request, level, message)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template, self.context)

    def post(
        self, request: HttpRequest, *args: str, **kwargs: Any
    ) -> HttpResponse | HttpResponseRedirect:
        new_password = request.POST.get("new_password")
        new_password_confirm = request.POST.get("new_password_confirm")

        try:
            token = Token.objects.get(id=request.session["token_id"])
            user = token.user

            if new_password == new_password_confirm:
                try:
                    if validate_password(new_password) is None:
                        user.set_password(new_password)
                        user.save()
                        request.session.delete("tokenUser")
                        return redirect("auth:login-view")
                except ValidationError as e:
                    self.context.update({"error_message": list(e.messages)})
                    return render(request, self.template, self.context, status=400)
            else:
                self.context.update(
                    {"error_message": ["Invalid input. Passwords do not match"]}
                )
                return render(request, self.template, self.context, status=400)
        except Exception:
            self.add_message(request, "Illegal request Detected.", messages.ERROR)
            return redirect("home-view")


class AuthLogoutView(LogoutView):
    next_page = reverse_lazy("home-view")
