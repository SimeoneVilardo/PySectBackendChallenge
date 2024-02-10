from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from server.apps.core.auth import CookieTokenAuthentication
from server.apps.core.filters.ChallengeFilter import ChallengeFilter
from server.apps.core.models import Challenge, Submission
from server.apps.core.models.user import User
from server.apps.core.serializers import ChallengeSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Prefetch

class ChallengePageNumberPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 100

class ChallengeView(GenericAPIView, ListModelMixin, RetrieveModelMixin):
    authentication_classes = (CookieTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ChallengeSerializer
    filterset_class = ChallengeFilter
    pagination_class = ChallengePageNumberPagination
    lookup_field = "id"

    def get_queryset(self):
        user: User = self.request.user
        return Challenge.users_objects.set_user(user)

    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)
