from django.contrib import admin
from .models import Challenge, Submission


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "subtitle", "points")
    search_fields = ("name",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "challenge", "status")
    search_fields = ("id", "challenge", "status")
