from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from server.apps.core.auth import CookieTokenAuthentication
from server.apps.core.models import Challenge, Submission
from server.apps.core.serializers import ChallengeSerializer
from django.db.models import Prefetch


class ChallengeView(GenericAPIView, ListModelMixin, RetrieveModelMixin):
    authentication_classes = (CookieTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ChallengeSerializer
    lookup_field = "id"

    def get_queryset(self):
        submissions = Submission.objects.filter(user=self.request.user)
        prefetch = Prefetch("submissions", queryset=submissions)
        return Challenge.objects.prefetch_related(prefetch)

    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)
