from rest_framework import serializers
from server.apps.core.models.challenge_submission import ChallengeSubmission


class ChallengeSubmissionResultSerializer(serializers.Serializer):
    output = serializers.CharField(write_only=True, required=True, allow_null=True, allow_blank=True)
    error = serializers.CharField(write_only=True, required=True, allow_null=True, allow_blank=True)
    challenge_submission_id = serializers.IntegerField(write_only=True, required=True)
