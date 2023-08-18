from django.contrib import admin

from resume.models import Resume, Social, Education, WorkHistory, Skill

# Register your models here.
admin.site.register(Resume)
admin.site.register(Social)
admin.site.register(Education)
admin.site.register(WorkHistory)
admin.site.register(Skill)
