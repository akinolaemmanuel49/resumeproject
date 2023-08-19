from django.urls import path

from resume.views import CreateResumeView


app_name = "resume"

urlpatterns = [
    path("create", CreateResumeView.as_view(), name="create-resume-view"),
]
