from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from resume.models import Resume

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

    def tearDown(self):
        self.user.delete()


class AddResumeSocialsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="janedoe@mail.com", password="testpassword123"
        )
        self.client.login(email="janedoe@mail.com", password="testpassword123")
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
        self.resume = Resume.objects.create(
            title="Python Developer",
            description="I am a python developer with over 3 years of experience. \nI have worked with professionals on projects that impacted the lives of people.",
            first_name="Jane",
            last_name="Doe",
            email="janedoe@mail.com",
            phone="000111000",
            user=self.user,
        )

    def test_add_resume_socials_view_get(self):
        response = self.client.get(reverse("resume:add-resume-socials"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resume/add-resume-socials.html")

    def test_add_resume_socials_view_post_success(self):
        session = self.client.session
        session["resume_id"] = self.resume.id
        session.save()
        data = {
            "name": ["LinkedIn", "Twitter"],
            "url": ["https://www.linkedin.com/janedoe", "https://twitter.com/janedoe"],
        }
        response = self.client.post(reverse("resume:add-resume-socials"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("resume:add-resume-education"))

    def test_add_resume_socials_view_post_resume_not_found(self):
        session = self.client.session
        session["resume_id"] = self.resume.id
        session.save()
        self.resume.delete()

        data = {
            "name": ["LinkedIn", "Twitter"],
            "url": ["https://www.linkedin.com/janedoe", "https://twitter.com/janedoe"],
        }
        response = self.client.post(reverse("resume:add-resume-socials"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("resume:create-resume-view"))

    def tearDown(self):
        try:
            if self.resume.id is not None:
                self.resume.delete()
        except Resume.DoesNotExist:
            pass
        self.user.delete()


class AddEducationViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="janedoe@mail.com", password="testpassword123"
        )
        self.client.login(email="janedoe@mail.com", password="testpassword123")
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
        self.resume = Resume.objects.create(
            title="Python Developer",
            description="I am a python developer with over 3 years of experience. \nI have worked with professionals on projects that impacted the lives of people.",
            first_name="Jane",
            last_name="Doe",
            email="janedoe@mail.com",
            phone="000111000",
            user=self.user,
        )

    def test_add_resume_education_view_get(self):
        response = self.client.get(reverse("resume:add-resume-education"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resume/add-resume-education.html")

    def test_add_resume_education_view_post_success(self):
        session = self.client.session
        session["resume_id"] = self.resume.id
        session.save()
        data = {
            "institution": ["Stanford University", "Cambridge University"],
            "start_date": ["2005-02-02", "2010-09-09"],
            "end_date": ["2010-02-02", "2012-09-09"],
            "degree": ["B.Sc. Computer Engineering", "M.Sc. Control Systems"],
        }
        response = self.client.post(reverse("resume:add-resume-education"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("resume:add-resume-work-history"))

    def test_add_resume_education_view_post_resume_not_found(self):
        session = self.client.session
        session["resume_id"] = self.resume.id
        session.save()
        self.resume.delete()

        data = {
            "institution": ["Stanford University", "Cambridge University"],
            "start_date": ["2005-02-02", "2010-09-09"],
            "end_date": ["2010-02-02", "2012-09-09"],
            "degree": ["B.Sc. Computer Engineering", "M.Sc. Control Systems"],
        }
        response = self.client.post(reverse("resume:add-resume-education"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("resume:create-resume-view"))

    def tearDown(self):
        try:
            if self.resume.id is not None:
                self.resume.delete()
        except Resume.DoesNotExist:
            pass
        self.user.delete()


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
