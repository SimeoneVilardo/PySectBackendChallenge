from django.contrib import admin
from .models import User, Challenge, ChallengeSubmission

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'reward')
    search_fields = ('name',)

@admin.register(ChallengeSubmission)
class ChallengeSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'challenge', 'src', 'output', 'error')
    search_fields = ('challenge',)