from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import User


# Create your models here.
class Resume(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    summary = models.TextField(_("Summary"), blank=True, null=True)
    first_name = models.CharField(_("First Name"), max_length=255)
    last_name = models.CharField(_("Last Name"), max_length=255)
    email = models.EmailField(_("Email Address"))
    phone = models.CharField(_("Phone Number"), max_length=15)
    image = models.ImageField(
        _("Resume Picture"),
        upload_to="images/resumes",
        blank=True,
        null=True,
        max_length=500,
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Social(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    url = models.URLField(_("URL"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=True)

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)


class Education(models.Model):
    institution = models.CharField(_("Institution Name"), max_length=255)
    start_date = models.CharField(_("Start Date"), max_length=7)  # Format: MM/YYYY
    end_date = models.CharField(_("End Date"), max_length=7)  # Format: MM/YYYY
    degree = models.CharField(_("Degree"), max_length=255)

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)


class WorkHistory(models.Model):
    name = models.CharField(_("Organization Name"), max_length=255)
    start_date = models.CharField(_("Start Date"), max_length=7)  # Format: MM/YYYY
    end_date = models.CharField(
        _("End Date"), max_length=7, blank=True, null=True
    )  # Optional
    position = models.CharField(_("Position"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=True)

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Work Histories"


class SkillGroup(models.Model):
    name = models.CharField(_("Skill Group Name"), max_length=255)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=True)

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="skill_groups")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "resume"], name="unique_skillgroup_per_resume"
            )
        ]


class Skill(models.Model):
    name = models.CharField(_("Skill Name"), max_length=255)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=True)

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    skill_group = models.ForeignKey(
        SkillGroup,
        on_delete=models.CASCADE,
        related_name="skills",  # Explicitly define the related_name
    )
