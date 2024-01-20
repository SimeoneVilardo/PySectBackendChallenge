from rest_framework import serializers
from server.apps.core.models.challenge_submission import ChallengeSubmission


class ChallengeSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeSubmission
        exclude = ("output",)
