from server.apps.core.models.challenge import Challenge
from server.apps.core.serializers.ChallengeSubmissionSerializer import ChallengeSubmissionSerializer
from rest_framework import serializers


class ChallengeSerializer(serializers.ModelSerializer):
    challenge_submissions = ChallengeSubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = Challenge
        exclude = ["input_path", "output_path"]
