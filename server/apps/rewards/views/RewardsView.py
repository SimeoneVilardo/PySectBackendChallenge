from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from server.apps.core.auth import CookieTokenAuthentication

from server.apps.rewards.models.reward import Reward
from server.apps.rewards.serializers import RewardSerializer


class RewardsView(GenericAPIView, ListModelMixin, RetrieveModelMixin):
    authentication_classes = (CookieTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RewardSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Reward.objects.all()
    
    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)