from django.test import TestCase, Client
from django.urls import reverse

from user.models import Profile, User


# Create your tests here.
class UserCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            email="janedoeduplicate@mail.com", password="testpassword123"
        )

    def test_user_create_view_get(self):
        response = self.client.get(reverse("user:create-user-view"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("user/register.html")

    def test_user_create_view_post_success(self):
        response = self.client.post(
            reverse("user:create-user-view"),
            {
                "email": "janedoe@mail.com",
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
                "email": "janedoe@mail.com",
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
                "email": "janedoeduplicate@mail.com",
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
                "email": "janedoe@mail.com",
                "password": "testpassword123",
                "confirm_password": "testpsssword123",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "user/register.html")

    def tearDown(self) -> None:
        self.user.delete()


class UserEditProfileViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            email="janedoe@mail.com", password="testpassword123"
        )
        self.client.login(email="janedoe@mail.com", password="testpassword123")

    def test_user_edit_profile_view_get(self) -> None:
        response = self.client.get(reverse("user:edit-profile-view"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/update-profile.html")

    def test_user_edit_profile_view_post_success(self) -> None:
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
        profile = Profile.objects.filter(user=self.user).first()
        self.assertIsInstance(profile, Profile)
        self.assertEqual(profile.first_name, "Jane")
        self.assertEqual(profile.last_name, "Doe")
        self.assertEqual(profile.email, "janedoe@mail.com")
        self.assertEqual(profile.phone, "000111000")

    def test_user_edit_profile_view_post_update_success(self) -> None:
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
        profile = Profile.objects.filter(user=self.user).first()
        self.assertIsInstance(profile, Profile)
        self.assertEqual(profile.first_name, "Jane")
        self.assertEqual(profile.last_name, "Doe")
        self.assertEqual(profile.email, "janedoe@mail.com")
        self.assertEqual(profile.phone, "000111000")
        response = self.client.post(
            reverse("user:edit-profile-view"),
            {
                "first_name": "Doe",
                "last_name": "Jane",
                "email": "doejane@mail.com",
                "phone": "111000111",
                "user": self.user,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user:profile-view"))
        profile = Profile.objects.filter(user=self.user).first()
        self.assertIsInstance(profile, Profile)
        self.assertEqual(profile.first_name, "Doe")
        self.assertEqual(profile.last_name, "Jane")
        self.assertEqual(profile.email, "doejane@mail.com")
        self.assertEqual(profile.phone, "111000111")

    def test_user_profile_view_get(self) -> None:
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

    def tearDown(self) -> None:
        self.user.delete()


class UserProfileViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            email="janedoe@mail.com", password="testpassword123"
        )
        self.client.login(email="janedoe@mail.com", password="testpassword123")

    def test_user_profile_view_get_profile_present(self) -> None:
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

    def test_user_profile_view_get_profile_absent(self) -> None:
        response = self.client.get((reverse("user:profile-view")))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user:edit-profile-view"))

    def tearDown(self) -> None:
        self.user.delete()
