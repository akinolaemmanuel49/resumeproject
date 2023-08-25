from django.urls import path

from resume.views import (
    AddEducationView,
    AddResumeSkillView,
    AddResumeSocialsView,
    AddWorkHistoryView,
    CreateResumeView,
    DownloadResumeAction,
    ResumePDFView,
    ResumeView,
    ResumesView,
)


app_name = "resume"

urlpatterns = [
    path("create/", CreateResumeView.as_view(), name="create-resume-view"),
    path("create/socials/", AddResumeSocialsView.as_view(), name="add-resume-socials"),
    path("create/education/", AddEducationView.as_view(), name="add-resume-education"),
    path(
        "create/work-history/",
        AddWorkHistoryView.as_view(),
        name="add-resume-work-history",
    ),
    path("create/skill/", AddResumeSkillView.as_view(), name="add-resume-skills"),
    path("resumes/", ResumesView.as_view(), name="resumes-view"),
    path("<int:id>/", ResumeView.as_view(), name="resume-view"),
    path(
        "<int:id>/preview/",
        ResumePDFView.as_view(),
        name="preview-pdf-resume-view",
    ),
    path(
        "<int:id>/download/",
        DownloadResumeAction.as_view(),
        name="download-resume-action",
    ),
]
