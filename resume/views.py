from typing import Any

from django.http import HttpRequest
from django.shortcuts import redirect, render, HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from user.models import Profile
from resume.models import Resume


# Create your views here.
class CreateResumeView(View, LoginRequiredMixin):
    template_name = "resume/create-resume.html"
    success_url = "account:dummy-view"
    page = "create-resume"
    title = "Create Resume"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return redirect("account:edit-profile-view")

        try:
            user_resumes = (
                Resume.objects.filter(user=request.user).all().order_by("-created_at")
            )
            dashboard_user_resumes = user_resumes[:3]
        except Resume.DoesNotExist:
            context = {
                "user_profile": user_profile,
                "page": self.page,
                "title": self.title,
            }
            return render(request, self.template_name, context)

        context = {
            "user_profile": user_profile,
            "dashboard_user_resumes": dashboard_user_resumes,
            "user_resumes": user_resumes,
            "page": self.page,
            "title": self.title,
        }

        return render(request, self.template_name, context)

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
            print("RESUME ID: ", resume.id)
            request.session["resume_id"] = resume.id
            return redirect(self.success_url)
        except Exception:
            try:
                user_profile = Profile.objects.get(user=request.user)
                context = {
                    "user_profile": user_profile,
                    "page": self.page,
                    "title": self.title,
                }
                return render(request, self.template_name, context)
            except Profile.DoesNotExist:
                context = {
                    "page": self.page,
                    "title": self.title,
                }
                return render(request, self.template_name, context)


class ResumesView(View, LoginRequiredMixin):
    template_name = "resume/resumes.html"
    page = "resumes"
    title = "Resumes"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            user_resumes = (
                Resume.objects.filter(user=request.user).all().order_by("-created_at")
            )
            dashboard_user_resumes = user_resumes[:3]
        except Resume.DoesNotExist:
            context = {
                "page": self.page,
                "title": self.title,
            }
            return render(request, self.template_name, context)

        context = {
            "dashboard_user_resumes": dashboard_user_resumes,
            "user_resumes": user_resumes,
            "page": self.page,
            "title": self.title,
        }

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        pass


class AddResumeSocialsView(View, LoginRequiredMixin):
    template_name = "resume/add-resume-socials.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        context = {
            "page": "create-resume",
            "title": "Add Resume Socials",
        }

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        pass
