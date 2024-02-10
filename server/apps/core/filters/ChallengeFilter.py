from server.apps.core.models import Challenge
from django_filters import rest_framework as filters

"""
class IsCompletedFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(is_completed=True)
"""

class ChallengeFilter(filters.FilterSet):
    is_completed = filters.BooleanFilter(label='is_completed')
    class Meta:
        model = Challenge
        fields = ['name', "is_completed"]
