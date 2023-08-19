from typing import Any

from django.http import HttpRequest
from django.shortcuts import redirect, render, HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from account.models import Profile
from resume.models import Resume


# Create your views here.
class CreateResumeView(View, LoginRequiredMixin):
    template_name = "resume/create-resume.html"
    success_url = "account:dummy-view"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        try:
            user_profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return render(request, self.template_name)

        context = {
            "user_profile": user_profile,
            "page": "create-resume",
            "title": "Create Resume",
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
                    "page": "create-resume",
                    "title": "Create Resume",
                }
                return render(request, self.template_name, context)
            except Profile.DoesNotExist:
                context = {
                    "page": "create-resume",
                    "title": "Create Resume",
                }
                return render(request, self.template_name, context)


class AddSocialsView(View, LoginRequiredMixin):
    template_name = "resume/add-socials.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        pass

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        pass
