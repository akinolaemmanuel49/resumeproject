from django.test import TestCase, Client
from django.urls import reverse

from user.models import Profile, User


# Create your tests here.
class AuthLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="janedoe@mail.com", password="testpassword123"
        )

    def test_login_view_get(self):
        response = self.client.get(reverse("auth:login-view"))
        self.assertEqual(response.status_code, 200)  # OK
        self.assertTemplateUsed(response, "auth/login.html")

    def test_login_view_post_success(self):
        response = self.client.post(
            reverse("auth:login-view"),
            {"email": "janedoe@mail.com", "password": "testpassword123"},
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse("user:edit-profile-view"))

    def test_login_view_post_next_page(self):
        next_page = "user:settings-view"
        response = self.client.post(
            reverse("auth:login-view") + f"?next={reverse(next_page)}",
            {"email": "janedoe@mail.com", "password": "testpassword123"},
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse("user:settings-view"))

    def test_login_view_post_unauthorized(self):
        response = self.client.post(
            reverse("auth:login-view"),
            {"email": "janedoe@mail.com", "password": "testpsssword123"},
        )
        self.assertEqual(response.status_code, 401)

    def test_login_view_post_profile_present(self):
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


class AuthLogoutViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            email="janedoe@mail.com", password="testpassword123"
        )
        self.client.login(email="janedoe@mail.com", password="testpassword123")

    def test_logout_view_success(self):
        response = self.client.post(
            reverse("auth:logout-view"),
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse("home-view"))

    def test_logout_view_anonymous_user(self):
        self.client.logout()
        response = self.client.post(
            reverse("auth:logout-view"),
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse("home-view"))

    def tearDown(self) -> None:
        self.user.delete()
