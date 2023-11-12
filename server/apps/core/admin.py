from django.contrib import admin
from .models import Challenge, ChallengeInput, ChallengeResult

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'reward')
    search_fields = ('name',)

@admin.register(ChallengeInput)
class ChallengeInputAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'challenge', 'files')
    search_fields = ('name',)

@admin.register(ChallengeResult)
class ChallengeResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'challenge', 'output', 'error')

    def has_add_permission(self, request):
        # Disable the 'Add' button
        return False

    def has_change_permission(self, request, obj=None):
        # Disable the 'Change' button
        return False

    def has_delete_permission(self, request, obj=None):
        # Disable the 'Delete' button
        return False