from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from server.apps.core.auth import CookieTokenAuthentication
from server.apps.rewards.models.reward import Reward
from server.apps.rewards.serializers import RedemptionSerializer
from rest_framework import serializers


class RedemptionView(ListAPIView, RetrieveAPIView, UpdateAPIView):
    authentication_classes = (CookieTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RedemptionSerializer
    lookup_field = "id"

    def get_object(self):
        return super().get_object()

    def get_queryset(self):
        if self.request.method == 'GET':
            return self.request.user.rewards.all()
        else:
            return Reward.objects.all()
    
    def perform_update(self, serializer):
        if self.request.user.remaining_points < serializer.instance.price:
            raise serializers.ValidationError("You do not have enough points to redeem this reward")
        return super().perform_update(serializer)