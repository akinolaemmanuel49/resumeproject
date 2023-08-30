from django.contrib.auth.base_user import BaseUserManager
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from pydantic import EmailStr, validate_email
from pydantic_core import PydanticCustomError


# Create your managers here.
class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of username.
    """

    def create_user(self, email: EmailStr, password: str, **extra_fields):
        """
        Create and save a user with the given email and password.

        Args:
            email (EmailStr): Email address for the user.
            password (str): Password for the user.
        """
        try:
            if not email:
                raise ValueError(_("The Email must be set."))
            email = self.normalize_email(email)
            # Validate email address.
            try:
                validate_email(email)
            except PydanticCustomError as e:
                raise e
            # Validate password.
            try:
                validate_password(password)
            except ValidationError as e:
                raise e
            # Create user object and save the instance to the database.
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save()
            return user
        # Handle exceptions.
        except Exception as e:
            raise e

    def create_superuser(self, email: EmailStr, password: str, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.

        Args:
            email (EmailStr): Email address for the super user.
            password (str): Password for the super user.
        """
        # Set extra fields values.
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
