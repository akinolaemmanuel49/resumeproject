from typing import Dict, List
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.core.mail import send_mail
from pydantic import EmailStr
import requests

from user.models import Profile, User


class ProtectedView(LoginRequiredMixin, View):
    template = None
    page = None
    title = None
    context = None
    next_page = None

    def add_message(self, request: HttpRequest, message: str, level=messages.INFO):
        messages.add_message(request, level, message)

    def dispatch_action(self, request, *args, **kwargs):
        try:
            User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            self.handle_no_permission()

    def handle_no_permission(self) -> HttpResponseRedirect:
        self.add_message(
            self.request, "You are not logged in. Please login.", messages.ERROR
        )
        if self.next_page:
            return redirect(
                reverse("auth:login-view") + f"?next={reverse(self.next_page)}"
            )
        return redirect(reverse("auth:login-view"))


def email_error_message_handler(error_message: str) -> list[str]:
    parts = error_message.split(":")

    if len(parts) == 2:
        _, description = parts
        error_message = [f"{description}"]
        return error_message
    else:
        return [error_message]


# def send_recover_password_mail(user_profile, recipient: EmailStr, variables: Dict[str, str]):
#     endpoint = f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN_NAME}/messages"
#     auth = ("api", settings.MAILGUN_API_KEY)
#     data = {
#         "from": f"Biteater0 <{settings.MAILGUN_POSTMASTER}>",
#         "to": [f"{user_profile.first_name} {user_profile.last_name}, <{recipient}>"],
#         "subject": "Recover your password",
#         "template": "password_reset",
#         **{f'v:{key}': value for key, value in variables.items()}
#     }
#     response = requests.post(endpoint, auth=auth, data=data)
#     return response

def send_recover_password_mail(user_profile, recipient: EmailStr, variables: Dict[str, str]):
    endpoint = f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN_NAME}/messages"
    auth = ("api", settings.MAILGUN_API_KEY)
    data = {
        "from": f"Biteater0 <{settings.MAILGUN_POSTMASTER}>",
        "to": [f"{recipient} <{recipient}>"],
        "subject": "Recover your password",
        "text": (
            f"Dear {variables['firstName']},\n\n"
            "We received a request to reset the password for your account associated with this email address. "
            "If you initiated this request, please click the link below to reset your password:\n\n"
            f"{variables['token']}\n\n"
            "This link will expire in 10 minutes for security purposes. If you did not request a password reset, "
            "please ignore this email or contact our support team at "
            f"{variables['support_email']}.\n\n"
            "Best regards,\n\n"
            f"{variables['company']} Support Team"
        )
    }
    response = requests.post(endpoint, auth=auth, data=data)
    print(response)
    return response