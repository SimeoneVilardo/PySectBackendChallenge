from server.apps.core.models import Submission
from django_filters import rest_framework as filters


class SubmissionFilter(filters.FilterSet):
    sort = filters.OrderingFilter(
        fields=(
            ("id", "id"),
            ("creation_date", "creation_date"),
        )
    )
