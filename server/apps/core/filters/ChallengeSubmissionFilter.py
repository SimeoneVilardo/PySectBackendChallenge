from server.apps.core.models import ChallengeSubmission
from django_filters import OrderingFilter, FilterSet


class ChallengeSubmissionFilter(FilterSet):
    sort = OrderingFilter(
        fields=(
            ("id", "id"),
            ("creation_date", "creation_date"),
        )
    )
