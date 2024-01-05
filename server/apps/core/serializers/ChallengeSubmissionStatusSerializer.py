from rest_framework import serializers

from server.apps.core.choices import ChallengeSubmissionStatusChoices


class ChallengeSubmissionStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    status = serializers.CharField()
