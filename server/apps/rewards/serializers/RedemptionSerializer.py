from server.apps.core.models.user import User
from server.apps.rewards.models.reward import Reward
from rest_framework import serializers


class RedemptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reward
        exclude = ('redemption',)
        read_only_fields = [f.name for f in Reward._meta.get_fields()]

    def validate(self, attrs):
        user: User = self.context.get("request").user
        if not self.instance.users.filter(id=user.id).exists():
            raise serializers.ValidationError('User must own the reward before attempting a redemption')
        return super().validate(attrs)

    def update(self, instance, validated_data):
        user: User = self.context.get("request").user
        instance.redemption.add(user)
        instance.save()
        return instance