from random import choice

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from user.managers import UserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _("Email address"),
        unique=True,
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Token(models.Model):
    token = models.CharField(_("Token"), blank=False, null=False, max_length=8)
    token_expires = models.DateTimeField(
        _("Token Expires"), default=timezone.now() + timezone.timedelta(minutes=10)
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def generate(self) -> str:
        numbers = [str(i) for i in range(10)]
        token = ""

        for __ in range(8):
            token += choice(numbers)

        self.token = token

        return token


class Profile(models.Model):
    first_name = models.CharField(_("First Name"), max_length=255)
    last_name = models.CharField(_("Last Name"), max_length=255)
    email = models.EmailField(_("Email Address"), unique=True)
    phone = models.CharField(_("Phone Number"), max_length=30, null=True)
    image = models.ImageField(
        _("Image"), upload_to="images/profiles", blank=True, null=True
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return f"{self.first_name}"
