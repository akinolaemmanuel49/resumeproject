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
        self.client.logout()


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
        response = self.client.get(reverse("user:profile-view"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user:edit-profile-view"))

    def tearDown(self) -> None:
        self.user.delete()
        self.client.logout()


class UserSettingsViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            email="janedoe@mail.com", password="testpassword123"
        )
        self.client.login(email="janedoe@mail.com", password="testpassword123")

    def test_user_settings_view_get(self) -> None:
        response = self.client.get(reverse("user:settings-view"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/settings.html")

    def tearDown(self) -> None:
        self.user.delete()
        self.client.logout()


class UserDeleteActionTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            email="janedoe@mail.com", password="testpassword123"
        )
        self.client.login(email="janedoe@mail.com", password="testpassword123")

    def test_user_delete_action_get_success(self) -> None:
        response = self.client.get(reverse("user:delete-user-action"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home-view"))

    def tearDown(self) -> None:
        self.user.delete()
        self.client.logout()


class UserChangeEmailActionTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            email="janedoe@mail.com", password="testpassword123"
        )
        self.client.login(email="janedoe@mail.com", password="testpassword123")

    def test_user_change_email_action_post_success(self) -> None:
        response = self.client.post(
            reverse("user:change-email-action"), {"new_email": "doejane@mail.com"}
        )
        self.client.logout()
        self.client.login(email="doejane@mail.com", password="testpassword123")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf-8"),
            {"Message": "User email was successfully changed."},
        )

    def test_user_change_email_action_post_invalid_email(self) -> None:
        response = self.client.post(
            reverse("user:change-email-action"), {"new_email": "doejanemail.com"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding="utf-8"),
            {"Error": "Invalid email address."},
        )

    def test_user_change_email_action_post_duplicate_email(self) -> None:
        self.client.post(
            reverse("user:create-user-view"),
            {
                "email": "janedoeduplicate@mail.com",
                "password": "testpassword123",
                "confirm_password": "testpassword123",
            },
        )
        response = self.client.post(
            reverse("user:change-email-action"),
            {"new_email": "janedoeduplicate@mail.com"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding="utf-8"),
            {"Error": "An account is already associated with this email address."},
        )

    def tearDown(self) -> None:
        self.user.delete()
        self.client.logout()


class UserChangePasswordActionTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            email="janedoe@mail.com", password="testpassword123"
        )
        self.client.login(email="janedoe@mail.com", password="testpassword123")

    def test_user_change_password_action_post_success(self) -> None:
        response = self.client.post(
            reverse("user:change-password-action"),
            {
                "old_password": "testpassword123",
                "new_password": "newtestpassword123",
                "new_password_confirm": "newtestpassword123",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf-8"),
            {"Message": "Password successfully changed."},
        )

    def test_user_change_password_action_post_passwords_mismatch(self) -> None:
        response = self.client.post(
            reverse("user:change-password-action"),
            {
                "old_password": "testpassword123",
                "new_password": "newtestpassword12",
                "new_password_confirm": "newtestpassword13",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding="utf-8"),
            {"Error": "Invalid input. Passwords do not match."},
        )

    def test_user_change_password_action_post_validation_error_below_minimum_length(
        self,
    ) -> None:
        response = self.client.post(
            reverse("user:change-password-action"),
            {
                "old_password": "testpassword123",
                "new_password": "A5m1r1",
                "new_password_confirm": "A5m1r1",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding="utf-8"),
            {
                "Error": [
                    "This password is too short. It must contain at least 8 characters."
                ]
            },
        )

    def test_user_change_password_action_post_validation_error_password_is_common(
        self,
    ) -> None:
        response = self.client.post(
            reverse("user:change-password-action"),
            {
                "old_password": "testpassword123",
                "new_password": "password",
                "new_password_confirm": "password",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding="utf-8"),
            {"Error": ["This password is too common."]},
        )

    def test_user_change_password_action_post_validation_error_password_is_numeric(
        self,
    ) -> None:
        response = self.client.post(
            reverse("user:change-password-action"),
            {
                "old_password": "testpassword123",
                "new_password": "01011122345",
                "new_password_confirm": "01011122345",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            str(response.content, encoding="utf-8"),
            {"Error": ["This password is entirely numeric."]},
        )

    def tearDown(self) -> None:
        self.user.delete()
        self.client.logout()
