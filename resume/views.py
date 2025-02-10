import base64
from typing import Any
import mimetypes

import tempfile
from weasyprint import HTML
from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import redirect, render, HttpResponse
from django.template.loader import render_to_string
from django.db import DatabaseError, IntegrityError
from django.db.transaction import TransactionManagementError

from user.models import Profile
from resume.models import Education, Resume, Skill, Social, WorkHistory
from resumeproject.utils import ProtectedView


# Create your views here.
class CreateResumeView(ProtectedView):
    template = "resume/create-resume.html"
    success_url = "resume:add-resume-socials"
    page = "create-resume"
    title = "Create Resume"
    context = {"title": title, "page": page}

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return redirect("user:edit-profile-view")

        try:
            user_resumes = (
                Resume.objects.filter(user=request.user).all().order_by("-created_at")
            )
        except Resume.DoesNotExist:
            self.context.update(
                {
                    "user_profile": user_profile,
                }
            )
            return render(request, self.template, self.context)

        self.context.update(
            {
                "user_profile": user_profile,
                "user_resumes": user_resumes,
            }
        )

        return render(request, self.template, self.context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        title = request.POST.get("title")
        description = request.POST.get("description")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        try:
            resume = Resume.objects.create(
                title=title,
                description=description,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                user=request.user,
            )

            if "image" in request.FILES:
                resume.image = request.FILES["image"]

            resume.save()
            request.session["resume_id"] = resume.id
            return redirect(self.success_url)
        except (Exception, DatabaseError, IntegrityError, TransactionManagementError):
            try:
                user_profile = Profile.objects.get(user=request.user)
                self.context.update(
                    {
                        "user_profile": user_profile,
                        "error_message": "An error occurred. \
                            Check the form and try again.",
                    }
                )
                return render(request, self.template, self.context, status=400)
            except Profile.DoesNotExist:
                return render(request, self.template, self.context, status=400)


class AddResumeSocialsView(ProtectedView):
    template = "resume/add-resume-socials.html"
    page = "create-resume"
    title = "Add Resume Socials"
    success_url = "resume:add-resume-education"
    context = {"title": title, "page": page}

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template, self.context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        names = request.POST.getlist("name")
        urls = request.POST.getlist("url")

        try:
            if request.session["resume_id"]:
                resume = Resume.objects.get(id=request.session["resume_id"])
            else:
                return redirect("resume:create-resume-view")
        except Resume.DoesNotExist:
            return redirect("resume:create-resume-view")
        for name, url in zip(names, urls):
            Social.objects.create(name=name, url=url, resume=resume)
        return redirect(self.success_url)


class AddEducationView(ProtectedView):
    template = "resume/add-resume-education.html"
    page = "create-resume"
    title = "Add Resume Educational Background"
    success_url = "resume:add-resume-work-history"
    context = {"title": title, "page": page}

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template, self.context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        institutions = request.POST.getlist("institution")
        start_dates = request.POST.getlist("start_date")
        end_dates = request.POST.getlist("end_date")
        degrees = request.POST.getlist("degree")

        try:
            if request.session["resume_id"]:
                resume = Resume.objects.get(id=request.session["resume_id"])
            else:
                return redirect("resume:create-resume-view")
        except Resume.DoesNotExist:
            return redirect("resume:create-resume-view")
        for institution, start_date, end_date, degree in zip(
            institutions, start_dates, end_dates, degrees
        ):
            Education.objects.create(
                institution=institution,
                start_date=start_date,
                end_date=end_date,
                degree=degree,
                resume=resume,
            )
        return redirect(self.success_url)


class AddWorkHistoryView(ProtectedView):
    template = "resume/add-resume-work-history.html"
    page = "create-resume"
    title = "Add Resume Work History"
    success_url = "resume:add-resume-skills"
    context = {"title": title, "page": page}

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template, self.context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        names = request.POST.getlist("organization_name")
        start_dates = request.POST.getlist("start_date")
        end_dates = request.POST.getlist("end_date")
        positions = request.POST.getlist("position")
        job_descriptions = request.POST.getlist("job_description")

        try:
            if request.session["resume_id"]:
                resume = Resume.objects.get(id=request.session["resume_id"])
            else:
                return redirect("resume:create-resume-view")
        except Resume.DoesNotExist:
            return redirect("resume:create-resume-view")

        for name, start_date, end_date, position, job_description in zip(
            names, start_dates, end_dates, positions, job_descriptions
        ):
            if end_date == "":
                end_date = None
            WorkHistory.objects.create(
                name=name,
                start_date=start_date,
                end_date=end_date,
                position=position,
                job_description=job_description,
                resume=resume,
            )
        return redirect(self.success_url)


class AddResumeSkillView(ProtectedView):
    template = "resume/add-resume-skill.html"
    page = "create-resume"
    title = "Add Resume Skill"
    success_url = "resume:resume-view"
    context = {"title": title, "page": page}

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request, self.template, self.context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        names = request.POST.getlist("name")
        levels = request.POST.getlist("level")

        try:
            if request.session["resume_id"]:
                resume = Resume.objects.get(id=request.session["resume_id"])
            else:
                return redirect("resume:create-resume-view")
        except Resume.DoesNotExist:
            return redirect("resume:create-resume-view")

        for name, level in zip(names, levels):
            Skill.objects.create(name=name, level=level, resume=resume)
        return redirect(self.success_url, id=resume.id)


class ResumesView(ProtectedView):
    template = "resume/resumes.html"
    page = "resumes"
    title = "Resumes"
    context = {"title": title, "page": page}

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            user_resumes = (
                Resume.objects.filter(user=request.user).all().order_by("-created_at")
            )
        except Resume.DoesNotExist:
            return render(request, self.template, self.context)

        self.context.update(
            {
                "user_resumes": user_resumes,
            }
        )

        return render(request, self.template, self.context)


class ResumeView(ProtectedView):
    template = "resume/resume-detail.html"
    page = "resumes"
    title = "Resume"
    context = {"title": title, "page": page}

    def get(
        self, request: HttpRequest, id: int, *args: str, **kwargs: Any
    ) -> HttpResponse:
        try:
            resume = Resume.objects.get(id=id)
            self.context.update({"resume": resume, "is_preview": True})
            return render(request, self.template, self.context)
        except Resume.DoesNotExist:
            return redirect("resume:create-resume-view")


class ResumePDFView(ProtectedView):
    template = "resume/resume-detail-pdf.html"
    page = "resumes"
    title = "Resume"
    context = {"title": title, "page": page}

    def get(
        self, request: HttpRequest, id: int, *args: str, **kwargs: Any
    ) -> HttpResponse:
        try:
            resume = Resume.objects.get(id=id)
            self.context.update(
                {
                    "resume": resume,
                    "is_preview": True,
                }
            )
            return render(request, self.template, self.context)
        except Resume.DoesNotExist:
            return redirect("resume:create-resume-view")


class DownloadResumeAction(ProtectedView):
    template = "resume/resume-detail-pdf.html"
    page = "resumes"
    title = "Resume"
    context = {"title": title, "page": page}

    def get(
        self, request: HttpRequest, id: int, *args: str, **kwargs: Any
    ) -> HttpResponse:
        options = {
            "page-size": "letter",
            "margin-top": "0.00001in",
            "margin-right": "0.00001in",
            "margin-bottom": "0.00001in",
            "margin-left": "0.00001in",
            "encoding": "UTF-8",
            "custom-header": [("Accept-Encoding", "gzip")],
            "no-outline": None,
        }
        try:
            resume = Resume.objects.get(id=id)
            image_url = request.build_absolute_uri(resume.image.url).replace("localhost", "127.0.0.1")

            # Get MIME type
            image_path = resume.image.path
            mime_type, _ = mimetypes.guess_type(image_path)
            mime_type = mime_type or "image/png"  # Default to PNG if unknown

            # Convert image to base64
            with open(image_path, "rb") as img_file:
                image_data = base64.b64encode(img_file.read()).decode("utf-8")

            self.context.update({
                "resume": resume,
                "image_base64": f"data:{mime_type};base64,{image_data}",
                "is_preview": False,
            })

            html_string = render_to_string(self.template, self.context)

            with tempfile.NamedTemporaryFile(delete=True) as output:
                HTML(string=html_string).write_pdf(output.name, options=options)
                output.seek(0)
                pdf = output.read()

            response = HttpResponse(pdf, content_type="application/pdf")
            response[
                "Content-Disposition"
            ] = f"attachment; filename={resume.first_name} {resume.last_name}'s Resume.pdf"
            return response
        except Resume.DoesNotExist:
            return HttpResponse(
                {"Error": "Resume not found."},
                content_type="application/json",
                status=404,
            )

class DeleteResumeAction(ProtectedView):
    success_url = "resume:resumes-view"
    page = "resumes"
    title = "Resume"
    context = {"title": title, "page": page}

    def get(
        self, request: HttpRequest, id: int, *args: str, **kwargs: Any
    ) -> HttpResponse:
        try:
            resume = Resume.objects.get(id=id, user=request.user)
            resume.delete()
            return redirect(self.success_url)
        except Resume.DoesNotExist:
            return redirect(self.success_url)
