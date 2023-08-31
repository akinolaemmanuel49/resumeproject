from django.contrib import admin

from user.models import Profile, Token, User

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Token)
