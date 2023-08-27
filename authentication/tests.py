from django.test import TestCase, Client
from django.urls import reverse

from user.models import Profile, User


# Create your tests here.
class AuthViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@mail.com", password="password"
        )
        self.profile = Profile.objects.create(user=self.user)

    def test_login_view_get(self):
        response = self.client.get(reverse("auth:login-view"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")

    def test_login_view_post_success(self):
        response = self.client.post(
            reverse("auth:login-view"),
            {"email": "testuser@mail.com", "password": "password"},
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse("user:profile-view"))

    def test_login_view_post_failure(self):
        response = self.client.post(
            reverse("auth:login-view"),
            {"email": "testuser@mail.com", "password": "psssword"},
        )
        self.assertEqual(response.status_code, 401)

    def test_logout_view(self):
        response = self.client.post(
            reverse("auth:logout-view"),
        )
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse("home-view"))

    def tearDown(self) -> None:
        self.profile.delete()
        self.user.delete()