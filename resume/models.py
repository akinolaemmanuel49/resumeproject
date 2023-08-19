from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User


# Create your models here.
class Resume(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    first_name = models.CharField(_("First Name"), max_length=255)
    last_name = models.CharField(_("Last Name"), max_length=255)
    email = models.EmailField(_("Email Address"))
    phone = models.CharField(_("Phone Number"), max_length=15)
    image = models.ImageField(
        _("Resume Picture"), upload_to="images/resumes", blank=True, null=True
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Social(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    url = models.URLField(_("URL"))

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)


class Education(models.Model):
    institution = models.CharField(_("Institution Name"), max_length=255)
    start_date = models.DateField(_("Start Date"))
    end_date = models.DateField(_("End Date"))
    degree = models.CharField(_("Degree"), max_length=255)

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)


class WorkHistory(models.Model):
    name = models.CharField(_("Organization Name"), max_length=255)
    start_date = models.DateField(_("Start Date"))
    end_date = models.DateField(_("End Date"), blank=True, null=True)
    position = models.CharField(_("Position"), max_length=255)

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Work Histories"


class Skill(models.Model):
    SKILL_CHOICES = (
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("expert", "Expert"),
    )
    name = models.CharField(_("Skill Name"), max_length=255)
    level = models.CharField(_("Level"), choices=SKILL_CHOICES, max_length=15)

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
