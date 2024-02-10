from server.apps.core.choices import SubmissionStatusChoices
from server.apps.core.models.challenge import Challenge
from rest_framework import serializers


class ChallengeSerializer(serializers.ModelSerializer):
    is_completed = serializers.BooleanField()

    class Meta:
        model = Challenge
        exclude = ["input", "output", "users"]
