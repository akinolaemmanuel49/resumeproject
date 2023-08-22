from typing import Any

from django.http import HttpRequest
from django.shortcuts import redirect, render, HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from user.models import Profile
from resume.models import Education, Resume, Social, WorkHistory


# Create your views here.
class CreateResumeView(View, LoginRequiredMixin):
    template_name = "resume/create-resume.html"
    success_url = "user:dummy-view"
    page = "create-resume"
    title = "Create Resume"

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
            context = {
                "user_profile": user_profile,
                "page": self.page,
                "title": self.title,
            }
            return render(request, self.template_name, context)

        context = {
            "user_profile": user_profile,
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
        except Resume.DoesNotExist:
            context = {
                "page": self.page,
                "title": self.title,
            }
            return render(request, self.template_name, context)

        context = {
            "user_resumes": user_resumes,
            "page": self.page,
            "title": self.title,
        }

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        pass


class ResumeView(View, LoginRequiredMixin):
    template_name = "resume/resume-view.html"
    page = "resumes"
    title = "Resume"

    def get(
        self, request: HttpRequest, id: int, *args: str, **kwargs: Any
    ) -> HttpResponse:
        try:
            resume = Resume.objects.get(id=id)
        except Resume.DoesNotExist:
            return HttpResponse("Error: 404.\nPage not found.")
        context = {"page": self.page, "title": self.title}
        return HttpResponse(
            f"Title: {resume.title}\n\
            Description: {resume.description}\n\
            Name: {resume.first_name} {resume.last_name}",
            context,
        )


class AddResumeSocialsView(View, LoginRequiredMixin):
    template_name = "resume/add-resume-socials.html"
    page = "create-resume"
    title = "Add Resume Socials"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        context = {
            "page": self.page,
            "title": self.title,
        }

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        names = request.POST.getlist("name")
        urls = request.POST.getlist("url")

        context = {
            "page": self.page,
            "title": self.title,
        }

        try:
            resume = Resume.objects.get(id=request.session["resume_id"])
        except Resume.DoesNotExist:
            return render(request, self.template_name, context)
        try:
            for name, url in zip(names, urls):
                Social.objects.create(name=name, url=url, resume=resume)
        except Exception:
            return render(request, self.template_name, context)
        return redirect("home-view")


class AddEducationView(View, LoginRequiredMixin):
    template_name = "resume/add-resume-education.html"
    page = "create-resume"
    title = "Add Resume Educational Background"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        context = {
            "page": self.page,
            "title": self.title,
        }

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        institutions = request.POST.getlist("institution")
        start_dates = request.POST.getlist("start_date")
        end_dates = request.POST.getlist("end_date")
        degrees = request.POST.getlist("degree")

        context = {
            "page": self.page,
            "title": self.title,
        }

        try:
            resume = Resume.objects.get(id=request.session["resume_id"])
        except Resume.DoesNotExist:
            return render(request, self.template_name, context)
        try:
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

        except Exception:
            return render(request, self.template_name, context)
        return redirect("home-view")


class AddWorkHistoryView(View, LoginRequiredMixin):
    template_name = "resume/add-resume-work-history.html"
    page = "create-resume"
    title = "Add Resume Work History"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        context = {
            "page": self.page,
            "title": self.title,
        }

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        names = request.POST.getlist("position")
        start_dates = request.POST.getlist("start_date")
        end_dates = request.POST.getlist("end_date")
        positions = request.POST.getlist("position")

        context = {
            "page": self.page,
            "title": self.title,
        }

        try:
            resume = Resume.objects.get(id=request.session["resume_id"])
        except Resume.DoesNotExist:
            return render(request, self.template_name, context)
        try:
            for name, start_date, end_date, position in zip(
                names, start_dates, end_dates, positions
            ):
                WorkHistory.objects.create(
                    name=name,
                    start_date=start_date,
                    end_date=end_date,
                    position=position,
                    resume=resume,
                )

        except Exception:
            return render(request, self.template_name, context)
        return redirect("home-view")
