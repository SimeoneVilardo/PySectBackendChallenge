from django.contrib import admin
from .models import Reward


@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "subtitle", "price")
    search_fields = ("name",)

