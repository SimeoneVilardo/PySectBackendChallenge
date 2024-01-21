from server.apps.core.models import Submission
from django_filters import OrderingFilter, FilterSet


class SubmissionFilter(FilterSet):
    sort = OrderingFilter(
        fields=(
            ("id", "id"),
            ("creation_date", "creation_date"),
        )
    )
