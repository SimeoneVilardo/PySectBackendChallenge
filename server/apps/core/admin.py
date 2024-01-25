from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from server.apps.core.models.user import User
from .models import Challenge, Submission

admin.site.register(User, UserAdmin)


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "subtitle", "points")
    search_fields = ("name",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "challenge", "status")
    search_fields = ("id", "challenge", "status")

