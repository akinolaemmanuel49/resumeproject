from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from resume.models import Education, Resume, Skill, Social, WorkHistory

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

    def test_add_resume_work_history_view_get(self):
        response = self.client.get(reverse("resume:add-resume-work-history"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resume/add-resume-work-history.html")

    def test_add_resume_work_history_view_post_success(self):
        session = self.client.session
        session["resume_id"] = self.resume.id
        session.save()
        data = {
            "organization_name": ["Catalina Systems", "Catalina Systems"],
            "start_date": ["2010-05-05", "2015-05-05"],
            "end_date": [
                "2015-05-05",
            ],
            "position": ["Backend Software Developer", "Systems Engineer"],
            "job_description": [
                "I was responsible for designing and documenting APIs.\nI handled the implementation of business logic for front-end client applications."
                "I was responsible for designing system architecture.\nI managed the implementation and testing of hardware systems ensuring they met product specifications and adhered to industry standards."
            ],
        }
        response = self.client.post(
            reverse("resume:add-resume-work-history"), data=data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("resume:add-resume-skills"))

    def test_add_resume_work_history_view_post_resume_not_found(self):
        session = self.client.session
        session["resume_id"] = self.resume.id
        session.save()
        self.resume.delete()

        data = {
            "organization_name": ["Catalina Systems", "Catalina Systems"],
            "start_date": ["2010-05-05", "2015-05-05"],
            "end_date": [
                "2015-05-05",
            ],
            "position": ["Backend Software Developer", "Systems Engineer"],
            "job_description": [
                "I was responsible for designing and documenting APIs.\nI handled the implementation of business logic for front-end client applications."
                "I was responsible for designing system architecture.\nI managed the implementation and testing of hardware systems ensuring they met product specifications and adhered to industry standards."
            ],
        }
        response = self.client.post(
            reverse("resume:add-resume-work-history"), data=data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("resume:create-resume-view"))

    def tearDown(self):
        try:
            if self.resume.id is not None:
                self.resume.delete()
        except Resume.DoesNotExist:
            pass
        self.user.delete()


class AddResumeSkillViewTestCase(TestCase):
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

    def test_add_resume_skill_view_get(self):
        response = self.client.get(reverse("resume:add-resume-skills"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resume/add-resume-skill.html")

    def test_add_resume_skill_view_post_success(self):
        session = self.client.session
        session["resume_id"] = self.resume.id
        session.save()
        data = {
            "name": ["Python", "C++", "C", "Hardware Design", "Project Management"],
            "level": [
                "intermediate",
                "intermediate",
                "intermediate",
                "intermediate",
                "intermediate",
            ],
        }
        response = self.client.post(reverse("resume:add-resume-skills"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("resume:resume-view", kwargs={"id": self.resume.id})
        )

    def test_add_resume_skill_view_post_resume_not_found(self):
        session = self.client.session
        session["resume_id"] = self.resume.id
        session.save()
        self.resume.delete()

        data = {
            "name": ["Python", "C++", "C", "Hardware Design", "Project Management"],
            "level": [
                "intermediate",
                "intermediate",
                "intermediate",
                "intermediate",
                "intermediate",
            ],
        }
        response = self.client.post(reverse("resume:add-resume-skills"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("resume:create-resume-view"))

    def tearDown(self):
        try:
            if self.resume.id is not None:
                self.resume.delete()
        except Resume.DoesNotExist:
            pass
        self.user.delete()


class ResumesViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="janedoe@mail.com", password="testpassword123"
        )
        self.client.login(email="janedoe@mail.com", password="testpassword123")

    def test_resumes_view_get_user_resumes_present(self):
        # Create two resumes using your template
        for i in range(1, 3):
            self.resume = Resume.objects.create(
                title=f"Resume {i}",
                description=f"This is the description for Resume {i}.",
                first_name="Jane",
                last_name="Doe",
                email=f"janedoe{i}@mail.com",
                phone=f"00011100{i}",
                user=self.user,
            )

            # Create associated objects for each resume
            Social.objects.create(
                name="LinkedIn",
                url=f"https://www.linkedin.com/janedoe{i}",
                resume=self.resume,
            )

            Education.objects.create(
                institution=f"Institution {i}",
                start_date="2005-02-02",
                end_date="2010-02-02",
                degree=f"B.Sc. Computer Science {i}",
                resume=self.resume,
            )

            WorkHistory.objects.create(
                name=f"Company {i}",
                start_date="2010-05-05",
                end_date="2015-05-05",
                position=f"Position {i}",
                job_description=f"I worked on projects {i}.\nI did this and that.",
                resume=self.resume,
            )

            Skill.objects.create(
                name=f"Skill {i}", level="intermediate", resume=self.resume
            )

        response = self.client.get(reverse("resume:resumes-view"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("user_resumes", response.context)
        self.assertContains(response, "Resume 1")
        self.assertContains(response, "Resume 2")

    def test_resumes_view_get_user_resumes_absent(self):
        response = self.client.get(reverse("resume:resumes-view"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Resume 1")
        self.assertNotContains(response, "Resume 2")

    def test_resumes_view_get_not_authorized(self):
        self.client.logout()
        response = self.client.get(reverse("resume:resumes-view"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("auth:login-view"))

    def tearDown(self):
        self.user.delete()


class ResumeViewTestCase(TestCase):
    pass


class ResumePDFViewTestCase(TestCase):
    pass


class DownloadResumeActionTestCase(TestCase):
    pass


class DeleteResumeActionTestCase(TestCase):
    pass
