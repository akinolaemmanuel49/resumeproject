from django.urls import path

from resume.views import AddResumeSocialsView, CreateResumeView, ResumesView


app_name = "resume"

urlpatterns = [
    path("create/", CreateResumeView.as_view(), name="create-resume-view"),
    path("create/socials/", AddResumeSocialsView.as_view(), name="add-resume-socials"),
    path("resumes/", ResumesView.as_view(), name="resumes-view"),
]
