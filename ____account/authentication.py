from typing import Any
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest
from pydantic import EmailStr

from account.models import User


class AuthenticationBackend(BaseBackend):
    def authenticate(
        self,
        request: HttpRequest,
        email: EmailStr | None = ...,
        password: str | None = ...,
        **kwargs: Any
    ) -> AbstractBaseUser | None:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id: int) -> AbstractBaseUser | None:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
