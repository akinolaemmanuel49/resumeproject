from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from user.models import User


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
        return redirect(reverse("auth:login-view") + f"?next={reverse(self.next_page)}")


def email_error_message_handler(error_message: str) -> list[str]:
    parts = error_message.split(":")

    if len(parts) == 2:
        _, description = parts
        error_message = [f"{description}"]
        return error_message
    else:
        return [error_message]
