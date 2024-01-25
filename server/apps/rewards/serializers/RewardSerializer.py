from server.apps.rewards.models.reward import Reward
from rest_framework import serializers


class RewardSerializer(serializers.ModelSerializer):
    is_redeemed = serializers.SerializerMethodField()

    class Meta:
        model = Reward
        exclude = ('redemption',)

    def get_is_redeemed(self, obj):
        user = self.context['request'].user
        return user.rewards.filter(id=obj.id).exists()