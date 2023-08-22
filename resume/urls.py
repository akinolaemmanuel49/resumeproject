from django.urls import path

from resume.views import (
    AddEducationView,
    AddResumeSocialsView,
    CreateResumeView,
    ResumeView,
    ResumesView,
)


app_name = "resume"

urlpatterns = [
    path("create/", CreateResumeView.as_view(), name="create-resume-view"),
    path("create/socials/", AddResumeSocialsView.as_view(), name="add-resume-socials"),
    path("create/education/", AddEducationView.as_view(), name="add-resume-education"),
    path("resumes/", ResumesView.as_view(), name="resumes-view"),
    path("<int:id>/", ResumeView.as_view(), name="resume-view"),
]
