from rest_framework import serializers
from server.apps.core.models.challenge_submission import ChallengeSubmission


class ChallengeSubmissionResultSerializer(serializers.Serializer):
    output = serializers.CharField(write_only=True, required=True, allow_null=False)
    error = serializers.CharField(write_only=True, required=False, allow_null=True)
