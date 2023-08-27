from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import login

from user.models import Profile, User


# Create your tests here.
class UserViewsTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@mail.com", password="testpassword123"
        )

    def test_user_create_view_get(self):
        response = self.client.get(reverse("user:create-user-view"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("user/register.html")

    def test_user_create_view_post_success(self):
        response = self.client.post(
            reverse("user:create-user-view"),
            {
                "email": "newtestuser@mail.com",
                "password": "testpassword123",
                "confirm_password": "testpassword123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("auth:login-view"))

    def test_user_create_view_post_password_validation_fail(self):
        response = self.client.post(
            reverse("user:create-user-view"),
            {
                "email": "testuser1@mail.com",
                "password": "password",
                "confirm_password": "password",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "user/register.html")

    def test_user_create_view_post_email_already_exists(self):
        response = self.client.post(
            reverse("user:create-user-view"),
            {
                "email": "testuser@mail.com",
                "password": "testpassword123",
                "confirm_password": "testpassword123",
            },
        )
        self.assertEqual(response.status_code, 409)
        self.assertTemplateUsed(response, "user/register.html")

    def test_user_create_view_post_passwords_do_not_match(self):
        response = self.client.post(
            reverse("user:create-user-view"),
            {
                "email": "testuser2@mail.com",
                "password": "testpassword123",
                "confirm_password": "testpsssword123",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "user/register.html")


class UserProfileViewsTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            email="janedoe@mail.com", password="testpassword123"
        )
        self.client.login(email="janedoe@mail.com", password="testpassword123")

    def test_user_edit_profile_view_get(self):
        response = self.client.get(reverse("user:edit-profile-view"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/update-profile.html")

    def test_user_edit_profile_view_login_required(self):
        self.client.logout()
        response = self.client.get(reverse("user:edit-profile-view"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("auth:login-view"))

    def test_user_edit_profile_view_post_successful(self):
        response = self.client.post(
            reverse("user:edit-profile-view"),
            {
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "janedoe@mail.com",
                "phone": "000111000",
                "user": self.user,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user:profile-view"))

    def test_user_edit_profile_view_post_update_successful(self):
        self.client.post(
            reverse("user:edit-profile-view"),
            {
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "janedoe@mail.com",
                "phone": "000111000",
                "user": self.user,
            },
        )
        if Profile.objects.filter(user=self.user).exists():
            profile = Profile.objects.filter(user=self.user).first()
            self.assertEqual(profile.first_name, "Jane")
            self.assertEqual(profile.last_name, "Doe")
            self.assertEqual(profile.email, "janedoe@mail.com")
            self.assertEqual(profile.phone, "000111000")

        response = self.client.post(
            reverse("user:edit-profile-view"),
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@mail.com",
                "phone": "111000111",
                "user": self.user,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user:profile-view"))

    def test_user_profile_view_get(self):
        self.client.post(
            reverse("user:edit-profile-view"),
            {
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "janedoe@mail.com",
                "phone": "000111000",
                "user": self.user,
            },
        )
        response = self.client.get(reverse("user:profile-view"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/profile.html")

    def tearDown(self):
        pass
