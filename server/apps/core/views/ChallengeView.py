from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from server.apps.core.models import Challenge
from server.apps.core.serializers import ChallengeSerializer


class ChallengeView(GenericAPIView, ListModelMixin, RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)
