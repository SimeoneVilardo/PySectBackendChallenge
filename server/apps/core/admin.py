from django.contrib import admin
from .models import Challenge, ChallengeSubmission


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "points")
    search_fields = ("name",)


@admin.register(ChallengeSubmission)
class ChallengeSubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "challenge")
    search_fields = ("challenge",)
