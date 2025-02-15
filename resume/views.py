import base64
from typing import Any
import mimetypes

import tempfile
from django.urls import reverse
from weasyprint import HTML
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.template.loader import render_to_string
from django.db import DatabaseError, IntegrityError
from django.db.transaction import TransactionManagementError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from resume.utils import validate_month_year_format
from user.models import Profile
from resume.models import Education, Resume, Skill, SkillGroup, Social, WorkHistory
from resumeproject.utils import ProtectedView


# Create your views here.
class CreateResumeView(ProtectedView):
    template = "resume/create-edit-resume.html"
    success_url = "resume:create-socials-view"
    failure_url = "resume:resume-view"
    page = "resume"
    title = "Resume"
    context = {"title": title, "page": page}

    # GET: Render the create or edit resume page based on resume_id
    def get(
        self, request: HttpRequest, id: int = None, *args: str, **kwargs: Any
    ) -> HttpResponse:
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return redirect("user:edit-profile-view")

        # If resume_id is not provided, render the form for creating a new resume
        if id is None:
            self.context.update(
                {
                    "user_profile": user_profile,
                    "action": "Create",  # Action will be 'Create' for new resumes
                    "method": "post",  # POST method for creating a new resume
                }
            )
            return render(request, self.template, self.context)

        return render(request, self.template, self.context)

    # POST: Handle creating a new resume
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        title = request.POST.get("title")
        summary = request.POST.get("summary")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        try:
            resume = Resume.objects.create(
                title=title,
                summary=summary,
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
        except (
            Exception,
            DatabaseError,
            IntegrityError,
            TransactionManagementError,
        ) as e:
            self.context.update(
                {
                    "error_message": "An error occurred. Check the form and try again.",
                }
            )
            return render(request, self.template, self.context, status=400)


class UpdateResumeView(ProtectedView):
    template = "resume/create-edit-resume.html"
    success_url = "resume:resume-detail-view"
    failure_url = "resume:resume-view"
    page = "resume"
    title = "Resume"
    context = {"title": title, "page": page}

    # GET: Render the edit resume page based on resume id
    def get(
        self, request: HttpRequest, resume_id: int, *args: str, **kwargs: Any
    ) -> HttpResponse:
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return redirect("user:edit-profile-view")

        # If resume id is provided, render the existing resume for editing
        try:
            resume = get_object_or_404(Resume, id=resume_id, user=request.user)
            self.context.update(
                {
                    "resume": resume,
                    "action": "Update",  # Action will be 'Update' for existing resumes
                    "method": "patch",  # PATCH method for updating an existing resume
                }
            )
        except Resume.DoesNotExist:
            return redirect(self.failure_url)

        return render(request, self.template, self.context)

    # POST: Handle updating an existing resume
    def post(
        self, request: HttpRequest, resume_id: int, *args: str, **kwargs: Any
    ) -> HttpResponse:
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)

        title = request.POST.get("title")
        summary = request.POST.get("summary")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        try:
            resume.title = title
            resume.summary = summary
            resume.first_name = first_name
            resume.last_name = last_name
            resume.email = email
            resume.phone = phone

            if "image" in request.FILES:
                resume.image = request.FILES["image"]

            resume.save()
            request.session["resume_id"] = resume.id
            return redirect(self.success_url)
        except (Exception, DatabaseError, IntegrityError, TransactionManagementError):
            self.context.update(
                {
                    "error_message": "An error occurred. Check the form and try again.",
                }
            )
            return render(request, self.template, self.context, status=400)


class CreateResumeSocialsView(ProtectedView):
    template = "resume/create-edit-resume-socials.html"
    page = "resume"
    title = "Resume Socials"
    success_url = "resume:create-education-view"
    failure_url = "resume:create-resume-view"
    context = {"title": title, "page": page}

    # POST: Handle creating new socials
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

    # GET: Handle getting the create socials form
    def get(
        self, request: HttpRequest, resume_id: int = None, *args: str, **kwargs: Any
    ) -> HttpResponse:
        if resume_id is None:
            self.context.update({"action": "Create"})
            return render(request, self.template, self.context)


class UpdateResumeSocialsView(ProtectedView):
    template = "resume/create-edit-resume-socials.html"
    page = "resume"
    title = "Resume Socials"
    success_url = "resume:resume-detail-view"
    failure_url = "resume:edit-socials-view"
    context = {"title": title, "page": page}

    # GET: Handle getting the update socials form
    def get(
        self, request: HttpRequest, resume_id: int, *args: str, **kwargs: Any
    ) -> HttpResponse:
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        socials = resume.social_set.all()
        self.context.update(
            {
                "resume": resume,
                "socials": socials,
                "action": "Edit",
            }
        )

        return render(request, self.template, self.context)

    def post(
        self, request: HttpRequest, resume_id: int, *args: str, **kwargs: Any
    ) -> HttpResponse:
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        social_ids = request.POST.getlist("social-id")  # Social IDs to keep
        names = request.POST.getlist("name")
        urls = request.POST.getlist("url")

        # Update existing socials
        for social_id, name, url in zip(social_ids, names, urls):
            if social_id.strip():  # Ensure the social_id is not empty
                social = get_object_or_404(Social, id=int(social_id), resume=resume)
                social.name = name
                social.url = url
                social.save()

        # Add new socials if the ID is empty
        for social_id, name, url in zip(social_ids, names, urls):
            if not social_id.strip():  # Check if it's an empty string
                if not Social.objects.filter(
                    name=name, url=url, resume=resume
                ).exists():
                    Social.objects.create(name=name, url=url, resume=resume)

        return redirect(self.success_url, resume_id)


class DeleteResumeSocialAction(ProtectedView):
    def post(
        self,
        request: HttpRequest,
        resume_id: int,
        social_id: int,
    ) -> HttpResponse:
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        social = get_object_or_404(Social, id=social_id, resume=resume)
        social.delete()
        return redirect(reverse("resume:edit-socials-view", args=[resume_id]))


class CreateEducationView(ProtectedView):
    template = "resume/create-edit-resume-education.html"
    page = "resume"
    title = "Resume Educational Background"
    success_url = "resume:create-work-history-view"
    context = {"title": title, "page": page}

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.context.update({"action": "Create"})
        return render(request, self.template, self.context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        institutions = request.POST.getlist("institution")
        start_dates = request.POST.getlist("start_date")
        end_dates = request.POST.getlist("end_date")
        degrees = request.POST.getlist("degree")

        try:
            for start_date, end_date in zip(start_dates, end_dates):
                validate_month_year_format(start_date)
                if end_date:
                    validate_month_year_format(end_date)
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


class UpdateEducationView(ProtectedView):
    template = "resume/create-edit-resume-education.html"
    page = "resume"
    title = "Resume Educational Background"
    success_url = "resume:resume-detail-view"
    context = {"title": title, "page": page}

    def get(
        self, request: HttpRequest, resume_id: int, *args: str, **kwargs: Any
    ) -> HttpResponse:
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        educations = resume.education_set.all()
        for education in educations:
            print(education.institution)
        self.context.update(
            {
                "resume": resume,
                "educations": educations,
                "action": "Edit",
            }
        )
        return render(request, self.template, self.context)

    def post(
        self, request: HttpRequest, resume_id: int, *args: str, **kwargs: Any
    ) -> HttpResponse:
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        education_ids = request.POST.getlist("education-id")
        institutions = request.POST.getlist("institution")
        start_dates = request.POST.getlist("start_date")
        end_dates = request.POST.getlist("end_date")
        degrees = request.POST.getlist("degree")

        for start_date, end_date in zip(start_dates, end_dates):
            validate_month_year_format(start_date)
            if end_date:
                validate_month_year_format(end_date)

        # Update existing educations
        for (
            education_id,
            institution,
            start_date,
            end_date,
            degree,
        ) in zip(
            education_ids,
            institutions,
            start_dates,
            end_dates,
            degrees,
        ):
            if education_id.strip():
                education = get_object_or_404(
                    Education, id=int(education_id), resume=resume
                )
                education.institution = institution
                education.start_date = start_date
                education.end_date = end_date
                education.degree = degree
                education.save()

        # Add new educations if the ID is empty
        for education_id, institution, start_date, end_date, degree in zip(
            education_ids, institutions, start_dates, end_dates, degrees
        ):
            if not education_id.strip():
                if not Education.objects.filter(
                    institution=institution,
                    start_date=start_date,
                    end_date=end_date,
                    degree=degree,
                    resume=resume,
                ).exists():
                    Education.objects.create(
                        institution=institution,
                        start_date=start_date,
                        end_date=end_date,
                        degree=degree,
                        resume=resume,
                    )

        return redirect(self.success_url, resume_id)


class DeleteResumeEducationAction(ProtectedView):
    def post(
        self,
        request: HttpRequest,
        resume_id: int,
        education_id: int,
    ) -> HttpResponse:
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        education = get_object_or_404(Education, id=education_id, resume=resume)
        education.delete()
        return redirect(reverse("resume:edit-education-view", args=[resume_id]))


class CreateWorkHistoryView(ProtectedView):
    template = "resume/create-edit-resume-work-history.html"
    page = "resume"
    title = "Resume Work History"
    success_url = "resume:create-skill-view"
    context = {"title": title, "page": page}

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.context.update({"action": "Create"})
        return render(request, self.template, self.context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        names = request.POST.getlist("organization_name")
        start_dates = request.POST.getlist("start_date")
        end_dates = request.POST.getlist("end_date")
        positions = request.POST.getlist("position")
        descriptions = request.POST.getlist("description")

        try:
            for start_date, end_date in zip(start_dates, end_dates):
                validate_month_year_format(start_date)
                if end_date:
                    validate_month_year_format(end_date)
            if request.session["resume_id"]:
                resume = Resume.objects.get(id=request.session["resume_id"])
            else:
                return redirect("resume:create-resume-view")
        except Resume.DoesNotExist:
            return redirect("resume:create-resume-view")

        for name, start_date, end_date, position, description in zip(
            names, start_dates, end_dates, positions, descriptions
        ):
            if end_date == "":
                end_date = None
            WorkHistory.objects.create(
                name=name,
                start_date=start_date,
                end_date=end_date,
                position=position,
                description=description,
                resume=resume,
            )
        return redirect(self.success_url)


class UpdateWorkHistoryView(ProtectedView):
    template = "resume/create-edit-resume-work-history.html"
    page = "resume"
    title = "Resume Work History"
    success_url = "resume:resume-detail-view"
    context = {"title": title, "page": page}

    def get(
        self, request: HttpRequest, resume_id: int, *args: str, **kwargs: Any
    ) -> HttpResponse:
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        work_histories = resume.workhistory_set.all()
        for work_history in work_histories:
            print(work_history.name)
        self.context.update(
            {
                "resume": resume,
                "work_histories": work_histories,
                "action": "Edit",
            }
        )
        return render(request, self.template, self.context)

    def post(
        self, request: HttpRequest, resume_id: int, *args: str, **kwargs: Any
    ) -> HttpResponse:
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        work_history_ids = request.POST.getlist("work-history-id")
        names = request.POST.getlist("organization_name")
        start_dates = request.POST.getlist("start_date")
        end_dates = request.POST.getlist("end_date")
        positions = request.POST.getlist("position")
        descriptions = request.POST.getlist("description")

        for start_date, end_date in zip(start_dates, end_dates):
            validate_month_year_format(start_date)
            if end_date:
                validate_month_year_format(end_date)

        # Update existing work histories
        for (
            work_history_id,
            name,
            start_date,
            end_date,
            position,
            description,
        ) in zip(
            work_history_ids,
            names,
            start_dates,
            end_dates,
            positions,
            descriptions,
        ):
            if work_history_id.strip():
                work_history = get_object_or_404(
                    WorkHistory, id=int(work_history_id), resume=resume
                )
                work_history.name = name
                work_history.start_date = start_date
                work_history.end_date = end_date
                work_history.position = position
                work_history.description = description
                work_history.save()

        # Add new work histories if the ID is empty
        for work_history_id, name, start_date, end_date, position, description in zip(
            work_history_ids, names, start_dates, end_dates, positions, descriptions
        ):
            if not work_history_id.strip():
                if not WorkHistory.objects.filter(
                    name=name,
                    start_date=start_date,
                    end_date=end_date,
                    position=position,
                    description=description,
                    resume=resume,
                ).exists():
                    WorkHistory.objects.create(
                        name=name,
                        start_date=start_date,
                        end_date=end_date,
                        position=position,
                        description=description,
                        resume=resume,
                    )

        return redirect(self.success_url, resume_id)


class DeleteResumeWorkHistoryAction(ProtectedView):
    def post(
        self,
        request: HttpRequest,
        resume_id: int,
        work_history_id: int,
    ) -> HttpResponse:
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        work_history = get_object_or_404(WorkHistory, id=work_history_id, resume=resume)
        work_history.delete()
        return redirect(reverse("resume:edit-work-history-view", args=[resume_id]))


class CreateResumeSkillView(ProtectedView):
    template_name = "resume/create-edit-resume-skill.html"
    success_url = "resume:resume-detail-view"

    def get(self, request, *args, **kwargs):
        resume = get_object_or_404(Resume, id=request.session.get("resume_id"))
        skill_groups = SkillGroup.objects.filter(resume=resume).prefetch_related(
            "skills"
        )
        context = {
            "action": "Create",
            "resume": resume,
            "skill_groups": skill_groups,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        resume = get_object_or_404(Resume, id=request.session.get("resume_id"))
        group_name = request.POST.get("group_name")
        skill_names = request.POST.getlist("skill_name")

        # Create a new Skill Group tied to the resume
        skill_group = SkillGroup.objects.create(name=group_name, resume=resume)

        # Add skills to the Skill Group
        for skill_name in skill_names:
            Skill.objects.create(name=skill_name, skill_group=skill_group)

        return redirect(self.success_url, resume.id)


class UpdateResumeSkillView(ProtectedView):
    template_name = "resume/create-edit-resume-skill.html"
    success_url = "resume:resume-detail-view"

    def get(self, request, resume_id, *args, **kwargs):
        resume = get_object_or_404(Resume, id=resume_id)
        skill_groups = SkillGroup.objects.filter(resume=resume).prefetch_related(
            "skills"
        )
        context = {
            "action": "Edit",
            "resume": resume,
            "skill_groups": skill_groups,
        }
        return render(request, self.template_name, context)

    def post(self, request, resume_id, *args, **kwargs):
        resume = get_object_or_404(Resume, id=resume_id)
        group_ids = request.POST.getlist("skill-group-id")
        group_names = request.POST.getlist("group_name")
        skill_ids = request.POST.getlist("skill-id")
        skill_names = request.POST.getlist("skill_name")

        # Update Skill Groups and Skills
        for group_id, group_name in zip(group_ids, group_names):
            skill_group = SkillGroup.objects.get(id=group_id, resume=resume)
            skill_group.name = group_name
            skill_group.save()

            # Update or Create Skills in the Skill Group
            for skill_id, skill_name in zip(skill_ids, skill_names):
                if skill_id:  # If skill_id is not empty, update the existing skill
                    try:
                        skill = Skill.objects.get(id=skill_id, skill_group=skill_group)
                        skill.name = skill_name
                        skill.save()
                    except Skill.DoesNotExist:
                        # Handle the case where the skill does not exist (optional)
                        pass
                else:  # If skill_id is empty, create a new skill
                    Skill.objects.create(
                        name=skill_name,
                        skill_group=skill_group,
                        resume=resume,  # Ensure the skill is tied to the resume
                    )

        return redirect("resume:resume-detail-view", resume.id)


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


class ResumeDetailView(ProtectedView):
    template = "resume/resume-detail.html"
    page = "resumes"
    title = "Resume"
    context = {"title": title, "page": page}

    def get(
        self, request: HttpRequest, id: int, *args: str, **kwargs: Any
    ) -> HttpResponse:
        try:
            resume = Resume.objects.get(id=id)
            skill_groups = SkillGroup.objects.filter(resume=resume).prefetch_related(
                "skills"
            )
            self.context.update(
                {
                    "resume": resume,
                    "skill_groups": skill_groups,
                    "is_preview": True,
                }
            )

            return render(request, self.template, self.context)
        except Resume.DoesNotExist:
            return redirect("resume:create-resume-view")


class ResumeDetailPDFView(ProtectedView):
    template = "resume/resume-detail-pdf.html"
    page = "resumes"
    title = "Resume"
    context = {"title": title, "page": page}

    def get(
        self, request: HttpRequest, id: int, *args: str, **kwargs: Any
    ) -> HttpResponse:
        try:
            resume = Resume.objects.get(id=id)
            skill_groups = SkillGroup.objects.filter(resume=resume).prefetch_related("skills")
            self.context.update(
                {
                    "resume": resume,
                    "skill_groups": skill_groups,
                    "is_preview": True,
                }
            )
            print("DEBUG")
            for skill_group in skill_groups:
                print(skill_group.name)
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
            skill_groups = SkillGroup.objects.filter(resume=resume).prefetch_related("skills")
            # image_url = request.build_absolute_uri(resume.image.url).replace(
            #     "localhost", "127.0.0.1"
            # )

            # Get MIME type
            if resume.image:
                image_path = resume.image.path
                mime_type, _ = mimetypes.guess_type(image_path)
                mime_type = mime_type or "image/png"  # Default to PNG if unknown

                # Convert image to base64
                with open(image_path, "rb") as img_file:
                    image_data = base64.b64encode(img_file.read()).decode("utf-8")

                self.context.update(
                    {
                        "resume": resume,
                        "skill_groups": skill_groups,
                        "image_base64": f"data:{mime_type};base64,{image_data}",
                        "is_preview": False,
                    }
                )
            else:
                self.context.update(
                    {
                        "resume": resume,
                        "is_preview": False,
                    }
                )

            html_string = render_to_string(self.template, self.context)

            with tempfile.NamedTemporaryFile(delete=True) as output:
                HTML(string=html_string).write_pdf(output.name, options=options)
                output.seek(0)
                pdf = output.read()

            response = HttpResponse(pdf, content_type="application/pdf")
            response["Content-Disposition"] = (
                f"attachment; filename={resume.first_name} {resume.last_name}'s Resume.pdf"
            )
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


@require_http_methods(["DELETE"])
def delete_skill(request, skill_id):
    try:
        skill = Skill.objects.get(id=skill_id)
        skill.delete()
        return JsonResponse({"success": True})
    except Skill.DoesNotExist:
        return JsonResponse({"success": False, "error": "Skill not found"}, status=404)


@require_http_methods(["DELETE"])
def delete_skill_group(request, group_id):
    try:
        skill_group = SkillGroup.objects.get(id=group_id)
        skill_group.delete()
        return JsonResponse({"success": True})
    except SkillGroup.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Skill Group not found"}, status=404
        )
