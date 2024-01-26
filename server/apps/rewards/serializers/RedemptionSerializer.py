from server.apps.core.models.user import User
from server.apps.rewards.models.reward import Reward
from rest_framework import serializers


class RedemptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reward
        exclude = ('redemption',)
        read_only_fields = [f.name for f in Reward._meta.get_fields()]

    def update(self, instance, validated_data):
        user: User = self.context.get("request").user
        instance.redemption.add(user)
        instance.save()
        return instance