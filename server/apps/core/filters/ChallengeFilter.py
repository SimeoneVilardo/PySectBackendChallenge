from server.apps.core.models import Challenge
from django_filters import rest_framework as filters


class ChallengeFilter(filters.FilterSet):
    is_completed = filters.BooleanFilter(label='is_completed')

    sort = filters.OrderingFilter(
        fields=(
            ("id", "id"),
            ("creation_date", "creation_date"),
        )
    )

    class Meta:
        model = Challenge
        fields = ['name', "points", "is_completed"]
