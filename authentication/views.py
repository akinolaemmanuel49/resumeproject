from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login

from user.models import Profile


# Create your views here.
class AuthLoginView(LoginView):
    template_name = "auth/login.html"
    title = "Login"
    context = {
        "title": title,
    }

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template_name, self.context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            try:
                next_page = request.GET.get('next')
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
            return render(request, self.template_name, self.context, status=401)


class AuthLogoutView(LogoutView):
    next_page = reverse_lazy("home-view")
