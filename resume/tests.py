from django.test import TestCase, Client
from django.urls import reverse
from unittest import skip

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
        self.assertTemplateUsed(response, "resume/create-edit-resume.html")

    def test_create_resume_view_get_profile_absent(self):
        response = self.client.get(reverse("resume:create-resume-view"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user:edit-profile-view"))

    def test_create_resume_view_post_success(self):
        response = self.client.post(
            reverse("resume:create-resume-view"),
            {
                "title": "Python Developer",
                "summary": "I am a python developer with over 3 years of experience. \nI have worked with professionals on projects that impacted the lives of people.",
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "janedoe@mail.com",
                "phone": "000111000",
                "user": self.user,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("resume:create-socials-view"))

    def tearDown(self):
        self.user.delete()


class CreateResumeSocialsViewTestCase(TestCase):
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
            summary="I am a python developer with over 3 years of experience. \nI have worked with professionals on projects that impacted the lives of people.",
            first_name="Jane",
            last_name="Doe",
            email="janedoe@mail.com",
            phone="000111000",
            user=self.user,
        )

    def test_add_resume_socials_view_get(self):
        response = self.client.get(reverse("resume:create-socials-view"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resume/create-edit-resume-socials.html")

    def test_add_resume_socials_view_post_success(self):
        session = self.client.session
        session["resume_id"] = self.resume.id
        session.save()
        data = {
            "name": ["LinkedIn", "Twitter"],
            "url": ["https://www.linkedin.com/janedoe", "https://twitter.com/janedoe"],
        }
        response = self.client.post(reverse("resume:create-socials-view"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("resume:create-education-view"))

    def test_add_resume_socials_view_post_resume_not_found(self):
        session = self.client.session
        session["resume_id"] = self.resume.id
        session.save()
        self.resume.delete()

        data = {
            "name": ["LinkedIn", "Twitter"],
            "url": ["https://www.linkedin.com/janedoe", "https://twitter.com/janedoe"],
        }
        response = self.client.post(reverse("resume:create-socials-view"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("resume:create-resume-view"))

    def tearDown(self):
        try:
            if self.resume.id is not None:
                self.resume.delete()
        except Resume.DoesNotExist:
            pass
        self.user.delete()


class CreateEducationViewTestCase(TestCase):
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
            summary="I am a python developer with over 3 years of experience. \nI have worked with professionals on projects that impacted the lives of people.",
            first_name="Jane",
            last_name="Doe",
            email="janedoe@mail.com",
            phone="000111000",
            user=self.user,
        )

    def test_add_resume_education_view_get(self):
        response = self.client.get(reverse("resume:create-education-view"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resume/create-edit-resume-education.html")

    def test_add_resume_education_view_post_success(self):
        session = self.client.session
        session["resume_id"] = self.resume.id
        session.save()
        data = {
            "institution": ["Stanford University", "Cambridge University"],
            "start_date": ["02/2005", "09/2010"],
            "end_date": ["02/2010", "09/2012"],
            "degree": ["B.Sc. Computer Engineering", "M.Sc. Control Systems"],
        }
        response = self.client.post(reverse("resume:create-education-view"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("resume:create-work-history-view")
        )

    def test_add_resume_education_view_post_resume_not_found(self):
        session = self.client.session
        session["resume_id"] = self.resume.id
        session.save()
        self.resume.delete()

        data = {
            "institution": ["Stanford University", "Cambridge University"],
            "start_date": ["02/2005", "09/2010"],
            "end_date": ["02/2010", "09/2012"],
            "degree": ["B.Sc. Computer Engineering", "M.Sc. Control Systems"],
        }
        response = self.client.post(reverse("resume:create-education-view"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("resume:create-resume-view"))

    def tearDown(self):
        try:
            if self.resume.id is not None:
                self.resume.delete()
        except Resume.DoesNotExist:
            pass
        self.user.delete()


class CreateWorkHistoryViewTestCase(TestCase):
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
            summary="I am a python developer with over 3 years of experience. \nI have worked with professionals on projects that impacted the lives of people.",
            first_name="Jane",
            last_name="Doe",
            email="janedoe@mail.com",
            phone="000111000",
            user=self.user,
        )

    def test_add_resume_work_history_view_get(self):
        response = self.client.get(reverse("resume:create-work-history-view"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resume/create-edit-resume-work-history.html")

    def test_add_resume_work_history_view_post_success(self):
        session = self.client.session
        session["resume_id"] = self.resume.id
        session.save()
        data = {
            "organization_name": ["Catalina Systems", "Catalina Systems"],
            "start_date": ["05/2010", "05/2015"],
            "end_date": [
                "05/2015",
            ],
            "position": ["Backend Software Developer", "Systems Engineer"],
            "description": [
                "I was responsible for designing and documenting APIs.\nI handled the implementation of business logic for front-end client applications."
                "I was responsible for designing system architecture.\nI managed the implementation and testing of hardware systems ensuring they met product specifications and adhered to industry standards."
            ],
        }
        response = self.client.post(
            reverse("resume:create-work-history-view"), data=data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("resume:create-skill-view"))

    def test_add_resume_work_history_view_post_resume_not_found(self):
        session = self.client.session
        session["resume_id"] = self.resume.id
        session.save()
        self.resume.delete()

        data = {
            "organization_name": ["Catalina Systems", "Catalina Systems"],
            "start_date": ["05/2010", "05/2015"],
            "end_date": [
                "05/2015",
            ],
            "position": ["Backend Software Developer", "Systems Engineer"],
            "description": [
                "I was responsible for designing and documenting APIs.\nI handled the implementation of business logic for front-end client applications."
                "I was responsible for designing system architecture.\nI managed the implementation and testing of hardware systems ensuring they met product specifications and adhered to industry standards."
            ],
        }
        response = self.client.post(
            reverse("resume:create-work-history-view"), data=data
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


# # Commentting out tests below this point
# class AddResumeSkillViewTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             email="janedoe@mail.com", password="testpassword123"
#         )
#         self.client.login(email="janedoe@mail.com", password="testpassword123")
#         self.client.post(
#             reverse("user:edit-profile-view"),
#             {
#                 "first_name": "Jane",
#                 "last_name": "Doe",
#                 "email": "janedoe@mail.com",
#                 "phone": "000111000",
#                 "user": self.user,
#             },
#         )
#         self.resume = Resume.objects.create(
#             title="Python Developer",
#             description="I am a python developer with over 3 years of experience. \nI have worked with professionals on projects that impacted the lives of people.",
#             first_name="Jane",
#             last_name="Doe",
#             email="janedoe@mail.com",
#             phone="000111000",
#             user=self.user,
#         )

#     def test_add_resume_skill_view_get(self):
#         response = self.client.get(reverse("resume:add-resume-skills"))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "resume/add-resume-skill.html")

#     def test_add_resume_skill_view_post_success(self):
#         session = self.client.session
#         session["resume_id"] = self.resume.id
#         session.save()
#         data = {
#             "name": ["Python", "C++", "C", "Hardware Design", "Project Management"],
#             "level": [
#                 "intermediate",
#                 "intermediate",
#                 "intermediate",
#                 "intermediate",
#                 "intermediate",
#             ],
#         }
#         response = self.client.post(reverse("resume:add-resume-skills"), data=data)
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(
#             response, reverse("resume:resume-view", kwargs={"id": self.resume.id})
#         )

#     def test_add_resume_skill_view_post_resume_not_found(self):
#         session = self.client.session
#         session["resume_id"] = self.resume.id
#         session.save()
#         self.resume.delete()

#         data = {
#             "name": ["Python", "C++", "C", "Hardware Design", "Project Management"],
#             "level": [
#                 "intermediate",
#                 "intermediate",
#                 "intermediate",
#                 "intermediate",
#                 "intermediate",
#             ],
#         }
#         response = self.client.post(reverse("resume:add-resume-skills"), data=data)
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse("resume:create-resume-view"))

#     def tearDown(self):
#         try:
#             if self.resume.id is not None:
#                 self.resume.delete()
#         except Resume.DoesNotExist:
#             pass
#         self.user.delete()


# class ResumesViewTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             email="janedoe@mail.com", password="testpassword123"
#         )
#         self.client.login(email="janedoe@mail.com", password="testpassword123")

#     def test_resumes_view_get_user_resumes_present(self):
#         # Create two resumes using your template
#         for i in range(1, 3):
#             resume = Resume.objects.create(
#                 title=f"Resume {i}",
#                 description=f"This is the description for Resume {i}.",
#                 first_name="Jane",
#                 last_name="Doe",
#                 email=f"janedoe{i}@mail.com",
#                 phone=f"00011100{i}",
#                 user=self.user,
#             )

#             # Create associated objects for each resume
#             Social.objects.create(
#                 name="LinkedIn",
#                 url=f"https://www.linkedin.com/janedoe{i}",
#                 resume=resume,
#             )

#             Education.objects.create(
#                 institution=f"Institution {i}",
#                 start_date="2005-02-02",
#                 end_date="2010-02-02",
#                 degree=f"B.Sc. Computer Science {i}",
#                 resume=resume,
#             )

#             WorkHistory.objects.create(
#                 name=f"Company {i}",
#                 start_date="2010-05-05",
#                 end_date="2015-05-05",
#                 position=f"Position {i}",
#                 job_description=f"I worked on projects {i}.\nI did this and that.",
#                 resume=resume,
#             )

#             Skill.objects.create(name=f"Skill {i}", level="intermediate", resume=resume)

#         response = self.client.get(reverse("resume:resumes-view"))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "resume/resumes.html")
#         self.assertIn("user_resumes", response.context)
#         self.assertContains(response, "Resume 1")
#         self.assertContains(response, "Resume 2")

#     def test_resumes_view_get_user_resumes_absent(self):
#         response = self.client.get(reverse("resume:resumes-view"))
#         self.assertEqual(response.status_code, 200)
#         self.assertNotContains(response, "Resume 1")
#         self.assertNotContains(response, "Resume 2")

#     def test_resumes_view_get_not_authorized(self):
#         self.client.logout()
#         response = self.client.get(reverse("resume:resumes-view"))
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse("auth:login-view"))

#     def tearDown(self):
#         self.user.delete()


# class ResumeViewTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             email="janedoe@mail.com", password="testpassword123"
#         )
#         self.client.login(email="janedoe@mail.com", password="testpassword123")
#         self.client.post(
#             reverse("user:edit-profile-view"),
#             {
#                 "first_name": "Jane",
#                 "last_name": "Doe",
#                 "email": "janedoe@mail.com",
#                 "phone": "000111000",
#                 "user": self.user,
#             },
#         )

#     def test_resume_view_get_resume_present(self):
#         resume = Resume.objects.create(
#             title="Resume 1",
#             description="This is the description for Resume 1.",
#             first_name="Jane",
#             last_name="Doe",
#             email="janedoe@mail.com",
#             phone="00011100",
#             user=self.user,
#         )

#         # Create associated objects for each resume
#         Social.objects.create(
#             name="LinkedIn",
#             url="https://www.linkedin.com/janedoe",
#             resume=resume,
#         )

#         Education.objects.create(
#             institution="Institution ",
#             start_date="2005-02-02",
#             end_date="2010-02-02",
#             degree="B.Sc. Computer Science",
#             resume=resume,
#         )

#         WorkHistory.objects.create(
#             name="Company 1",
#             start_date="2010-05-05",
#             end_date="2015-05-05",
#             position="Position 1",
#             job_description="I worked on projects 1.\nI did this and that.",
#             resume=resume,
#         )

#         Skill.objects.create(name="Skill ", level="intermediate", resume=resume)

#         response = self.client.get(
#             reverse("resume:resume-view", kwargs={"id": resume.id})
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "resume/resume-detail.html")
#         self.assertIn("resume", response.context)
#         self.assertIn("is_preview", response.context)
#         self.assertContains(response, "Resume 1")

#     def test_resume_view_get_resume_absent(self):
#         response = self.client.get(reverse("resume:resume-view", kwargs={"id": 1}))
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse("resume:create-resume-view"))

#     def tearDown(self):
#         self.user.delete()


# class ResumePDFViewTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             email="janedoe@mail.com", password="testpassword123"
#         )
#         self.client.login(email="janedoe@mail.com", password="testpassword123")
#         self.client.post(
#             reverse("user:edit-profile-view"),
#             {
#                 "first_name": "Jane",
#                 "last_name": "Doe",
#                 "email": "janedoe@mail.com",
#                 "phone": "000111000",
#                 "user": self.user,
#             },
#         )

#     def test_resume_pdf_view_get_resume_present(self):
#         resume = Resume.objects.create(
#             title="Resume 1",
#             description="This is the description for Resume 1.",
#             first_name="Jane",
#             last_name="Doe",
#             email="janedoe@mail.com",
#             phone="00011100",
#             user=self.user,
#         )

#         # Create associated objects for each resume
#         Social.objects.create(
#             name="LinkedIn",
#             url="https://www.linkedin.com/janedoe",
#             resume=resume,
#         )

#         Education.objects.create(
#             institution="Institution ",
#             start_date="02/2005",
#             end_date="02/2010",
#             degree="B.Sc. Computer Science",
#             resume=resume,
#         )

#         WorkHistory.objects.create(
#             name="Company 1",
#             start_date="05/2010",
#             end_date="05/2015",
#             position="Position 1",
#             description="I worked on projects 1.\nI did this and that.",
#             resume=resume,
#         )

#         Skill.objects.create(name="Skill ", level="intermediate", resume=resume)

#         response = self.client.get(
#             reverse("resume:preview-pdf-resume-view", kwargs={"id": resume.id})
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "resume/resume-detail-pdf.html")
#         self.assertIn("resume", response.context)
#         self.assertIn("is_preview", response.context)
#         self.assertContains(response, "Resume 1")

#     def test_resume_pdf_view_get_resume_absent(self):
#         response = self.client.get(
#             reverse("resume:preview-pdf-resume-view", kwargs={"id": 1})
#         )
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse("resume:create-resume-view"))

#     def tearDown(self):
#         self.user.delete()


# class DownloadResumeActionTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             email="janedoe@mail.com", password="testpassword123"
#         )

#         self.client.login(email="janedoe@mail.com", password="testpassword123")
#         self.client.post(
#             reverse("user:edit-profile-view"),
#             {
#                 "first_name": "Jane",
#                 "last_name": "Doe",
#                 "email": "janedoe@mail.com",
#                 "phone": "000111000",
#                 "user": self.user,
#             },
#         )

#     @skip
#     def test_download_resume_action_resume_present(self):
#         resume = Resume.objects.create(
#             title="Resume 1",
#             description="This is the description for Resume 1.",
#             first_name="Jane",
#             last_name="Doe",
#             email="janedoe@mail.com",
#             phone="00011100",
#             user=self.user,
#         )

#         # Create associated objects for each resume
#         Social.objects.create(
#             name="LinkedIn",
#             url="https://www.linkedin.com/janedoe",
#             resume=resume,
#         )

#         Education.objects.create(
#             institution="Institution ",
#             start_date="2005-02-02",
#             end_date="2010-02-02",
#             degree="B.Sc. Computer Science",
#             resume=resume,
#         )

#         WorkHistory.objects.create(
#             name="Company 1",
#             start_date="2010-05-05",
#             end_date="2015-05-05",
#             position="Position 1",
#             job_description="I worked on projects 1.\nI did this and that.",
#             resume=resume,
#         )

#         Skill.objects.create(name="Skill ", level="intermediate", resume=resume)

#         response = self.client.get(
#             reverse("resume:download-resume-action", kwargs={"id": resume.id})
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response["Content-Type"], "application/pdf")
#         expected_filename = f"{resume.first_name} {resume.last_name}'s Resume.pdf"
#         self.assertIn(
#             f"attachment; filename={expected_filename}",
#             response["Content-Disposition"],
#         )
#         self.assertTrue(len(response.content) > 0)

#     def test_download_resume_action_resume_absent(self):
#         response = self.client.get(
#             reverse("resume:download-resume-action", kwargs={"id": 1})
#         )
#         self.assertEqual(response.status_code, 404)


# class DeleteResumeActionTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             email="janedoe@mail.com", password="testpassword123"
#         )
#         self.client.login(email="janedoe@mail.com", password="testpassword123")
#         self.client.post(
#             reverse("user:edit-profile-view"),
#             {
#                 "first_name": "Jane",
#                 "last_name": "Doe",
#                 "email": "janedoe@mail.com",
#                 "phone": "000111000",
#                 "user": self.user,
#             },
#         )

#     def test_delete_resume_action_resume_present(self):
#         resume = Resume.objects.create(
#             title="Resume 1",
#             description="This is the description for Resume 1.",
#             first_name="Jane",
#             last_name="Doe",
#             email="janedoe@mail.com",
#             phone="00011100",
#             user=self.user,
#         )

#         # Create associated objects for each resume
#         Social.objects.create(
#             name="LinkedIn",
#             url="https://www.linkedin.com/janedoe",
#             resume=resume,
#         )

#         Education.objects.create(
#             institution="Institution ",
#             start_date="2005-02-02",
#             end_date="2010-02-02",
#             degree="B.Sc. Computer Science",
#             resume=resume,
#         )

#         WorkHistory.objects.create(
#             name="Company 1",
#             start_date="2010-05-05",
#             end_date="2015-05-05",
#             position="Position 1",
#             job_description="I worked on projects 1.\nI did this and that.",
#             resume=resume,
#         )

#         Skill.objects.create(name="Skill ", level="intermediate", resume=resume)

#         response = self.client.get(
#             reverse("resume:delete-resume-action", kwargs={"id": resume.id})
#         )
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse("resume:resumes-view"))

#     def test_delete_resume_action_resume_absent(self):
#         response = self.client.get(
#             reverse("resume:delete-resume-action", kwargs={"id": 1})
#         )
#         self.assertEqual(response.status_code, 302)
#         self.assertRedirects(response, reverse("resume:resumes-view"))
