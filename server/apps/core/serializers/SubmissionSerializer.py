from rest_framework import serializers
from server.apps.core.models.submission import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        exclude = ("output",)
