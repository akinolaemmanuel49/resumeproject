from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from user.models import User


# Create your tests here.
class CreateResumeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="janedoe@mail.com", password="testpassword123"
        )
        self.client.login(email="janedoe@mail.com", password="testpassword123")

    def test_create_resume_view_get_profile_present(self):
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
        response = self.client.get(reverse("resume:create-resume-view"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resume/create-resume.html")

    def test_create_resume_view_get_profile_absent(self):
        response = self.client.get(reverse("resume:create-resume-view"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user:edit-profile-view"))

    def test_create_resume_view_post_success(self):
        response = self.client.post(
            reverse("resume:create-resume-view"),
            {
                "title": "Python Developer",
                "description": "I am a python developer with over 3 years of experience. \nI have worked with professionals on projects that impacted the lives of people.",
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "janedoe@mail.com",
                "phone": "000111000",
                "user": self.user,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("resume:add-resume-socials"))


class AddResumeSocialsViewTestCase(TestCase):
    pass

class AddEducationViewTestCase(TestCase):
    pass


class AddWorkHistoryViewTestCase(TestCase):
    pass


class AddResumeSkillViewTestCase(TestCase):
    pass


class ResumesViewTestCase(TestCase):
    pass


class ResumeViewTestCase(TestCase):
    pass


class ResumePDFViewTestCase(TestCase):
    pass


class DownloadResumeActionTestCase(TestCase):
    pass


class DeleteResumeActionTestCase(TestCase):
    pass
