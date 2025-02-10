from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from user.models import Profile, Token, User


# Create your tests here.
class AuthLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="janedoe@mail.com", password="testpassword123"
        )

    def test_auth_login_view_get(self):
        response = self.client.get(reverse("auth:login-view"))
        self.assertEqual(response.status_code, 200)  # OK
        self.assertTemplateUsed(response, "auth/login.html")

    def test_auth_login_view_post_success(self):
        response = self.client.post(
            reverse("auth:login-view"),
            {"email": "janedoe@mail.com", "password": "testpassword123"},
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse("user:edit-profile-view"))

    def test_auth_login_view_post_next_page(self):
        next_page = "user:settings-view"
        response = self.client.post(
            reverse("auth:login-view") + f"?next={reverse(next_page)}",
            {"email": "janedoe@mail.com", "password": "testpassword123"},
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse("user:settings-view"))

    def test_auth_login_view_post_unauthorized(self):
        response = self.client.post(
            reverse("auth:login-view"),
            {"email": "janedoe@mail.com", "password": "testpsssword123"},
        )
        self.assertEqual(response.status_code, 401)

    def test_auth_login_view_post_profile_present(self):
        profile = Profile.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="janedoe@mail.com",
            phone="111222333",
            user=self.user,
        )
        profile.save()
        response = self.client.post(
            reverse("auth:login-view"),
            {"email": "janedoe@mail.com", "password": "testpassword123"},
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse("user:profile-view"))

    def tearDown(self) -> None:
        self.user.delete()

class AuthResetPasswordGetEmailViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            email="janedoe@mail.com", password="testpassword123"
        )

    def test_auth_reset_password_get_email_view_get(self):
        response = self.client.get(reverse("auth:password-reset-get-email"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/password_reset_email.html")

    def test_auth_reset_password_get_email_view_profile_not_found(self):
        response = self.client.post(
            reverse("auth:password-reset-get-email"), {"email": "janedoe@mail.com"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user:create-user-view"))

    def test_auth_reset_password_get_email_view_post_user_not_found(self):
        response = self.client.post(
            reverse("auth:password-reset-get-email"), {"email": "johndoe@mail.com"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/password_reset_email.html")
        self.assertContains(response, "User not found.")

    def tearDown(self) -> None:
        self.user.delete()


class AuthResetPasswordSetTokenViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            email="janedoe@mail.com", password="testpassword123"
        )
        self.client.post(
            reverse("auth:password-reset-get-email"), {"email": "janedoe@mail.com"}
        )
        self.token = Token.objects.create(
            token="12345678",
            token_expires=timezone.now() + timezone.timedelta(minutes=10),
            user=self.user,
        )
        self.expired_token = Token.objects.create(
            token="12345679",
            token_expires=timezone.now() - timezone.timedelta(minutes=10),
            user=self.user,
        )
        self.token.save()

    def test_auth_reset_password_set_token_view_get(self):
        response = self.client.get(reverse("auth:password-reset-set-token"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/password_reset_token.html")

    def test_auth_reset_password_set_token_view_post_success(self):
        response = self.client.post(
            reverse("auth:password-reset-set-token"), {"token": self.token.token}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("auth:password-reset"))

    def test_auth_reset_password_set_token_view_post_invalid_token(self):
        response = self.client.post(
            reverse("auth:password-reset-set-token"), {"token": "12345677"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/password_reset_token.html")
        self.assertContains(response, "Invalid or expired token.")

    def test_auth_reset_password_set_token_view_post_expired_token(self):
        response = self.client.post(
            reverse("auth:password-reset-set-token"),
            {"token": self.expired_token.token},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/password_reset_token.html")
        self.assertContains(response, "Invalid or expired token.")


class AuthResetPasswordResetViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            email="janedoe@mail.com", password="testpassword123"
        )

    def test_auth_reset_password_reset_view_get(self):
        response = self.client.get(reverse("auth:password-reset"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/password_reset_password.html")

    def test_auth_reset_password_reset_view_post_success(self):
        self.client.post(
            reverse("auth:password-reset-get-email"), {"email": "janedoe@mail.com"}
        )
        token = Token.objects.create(
            token="12345678",
            token_expires=timezone.now() + timezone.timedelta(minutes=10),
            user=self.user,
        )
        self.client.post(
            reverse("auth:password-reset-set-token"), {"token": token.token}
        )
        response = self.client.post(
            reverse("auth:password-reset"),
            {
                "new_password": "newtestpassword123",
                "new_password_confirm": "newtestpassword123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("auth:login-view"))

    def test_auth_reset_password_reset_view_post_illegal_request(self):
        response = self.client.post(
            reverse("auth:password-reset"),
            {
                "new_password": "newtestpassword123",
                "new_password_confirm": "newtestpassword123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home-view"))

    def test_auth_reset_password_reset_view_post_password_mismatch(self):
        self.client.post(
            reverse("auth:password-reset-get-email"), {"email": "janedoe@mail.com"}
        )
        token = Token.objects.create(
            token="12345678",
            token_expires=timezone.now() + timezone.timedelta(minutes=10),
            user=self.user,
        )
        self.client.post(
            reverse("auth:password-reset-set-token"), {"token": token.token}
        )
        response = self.client.post(
            reverse("auth:password-reset"),
            {
                "new_password": "newtestpassword",
                "new_password_confirm": "newtestpassword123",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "auth/password_reset_password.html")
        self.assertContains(
            response, "Invalid input. Passwords do not match", status_code=400
        )

    def test_auth_reset_password_reset_view_post_password_validation_common(self):
        self.client.post(
            reverse("auth:password-reset-get-email"), {"email": "janedoe@mail.com"}
        )
        token = Token.objects.create(
            token="12345678",
            token_expires=timezone.now() + timezone.timedelta(minutes=10),
            user=self.user,
        )
        self.client.post(
            reverse("auth:password-reset-set-token"), {"token": token.token}
        )
        response = self.client.post(
            reverse("auth:password-reset"),
            {
                "new_password": "password",
                "new_password_confirm": "password",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "auth/password_reset_password.html")
        self.assertContains(response, "This password is too common.", status_code=400)

    def test_auth_reset_password_reset_view_post_password_validation_short(self):
        self.client.post(
            reverse("auth:password-reset-get-email"), {"email": "janedoe@mail.com"}
        )
        token = Token.objects.create(
            token="12345678",
            token_expires=timezone.now() + timezone.timedelta(minutes=10),
            user=self.user,
        )
        self.client.post(
            reverse("auth:password-reset-set-token"), {"token": token.token}
        )
        response = self.client.post(
            reverse("auth:password-reset"),
            {
                "new_password": "A5m1r1",
                "new_password_confirm": "A5m1r1",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "auth/password_reset_password.html")
        self.assertContains(
            response,
            "This password is too short. It must contain at least 8 characters.",
            status_code=400,
        )

    def test_auth_reset_password_reset_view_post_password_validation_numeric(self):
        self.client.post(
            reverse("auth:password-reset-get-email"), {"email": "janedoe@mail.com"}
        )
        token = Token.objects.create(
            token="12345678",
            token_expires=timezone.now() + timezone.timedelta(minutes=10),
            user=self.user,
        )
        self.client.post(
            reverse("auth:password-reset-set-token"), {"token": token.token}
        )
        response = self.client.post(
            reverse("auth:password-reset"),
            {
                "new_password": "01011122345",
                "new_password_confirm": "01011122345",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "auth/password_reset_password.html")
        self.assertContains(
            response, "This password is entirely numeric.", status_code=400
        )


class AuthLogoutViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            email="janedoe@mail.com", password="testpassword123"
        )
        self.client.login(email="janedoe@mail.com", password="testpassword123")

    def test_auth_logout_view_success(self):
        response = self.client.post(
            reverse("auth:logout-view"),
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse("home-view"))

    def test_auth_logout_view_anonymous_user(self):
        self.client.logout()
        response = self.client.post(
            reverse("auth:logout-view"),
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse("home-view"))

    def tearDown(self) -> None:
        self.user.delete()
