from resume.models import Resume


def dashboard_resumes(request):
    context = {}

    if request.user.is_authenticated:
        context["dashboard_user_resumes"] = Resume.objects.filter(
            user=request.user
        ).order_by("-created_at")[:3]

    return context
