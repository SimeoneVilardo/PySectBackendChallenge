from datetime import datetime
import os
from django.conf import settings
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.contrib.auth.models import User
from server.apps.core.models import Challenge, ChallengeSubmission


class ChallengeSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeSubmission
        fields = "__all__"


class ChallengeSubmissionFileSerializer(serializers.Serializer):
    file = serializers.FileField()


class ChallengeSubmissionCreateView(generics.CreateAPIView):
    serializer_class = ChallengeSubmissionFileSerializer
    queryset = ChallengeSubmission.objects.all()
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        file_obj = request.data.get("file")
        user_id = 1  # dummy user id
        src_path = "dummy.py"  # dummy src path

        if not file_obj:
            return Response({"error": "No file received"}, status=status.HTTP_400_BAD_REQUEST)

        challenge = Challenge.objects.get(id=kwargs["id"])
        user = User.objects.get(id=user_id)
        challenge_submission = self.create_challenge_submission(challenge, user, src_path)
        return Response(status=status.HTTP_201_CREATED)

    def create_challenge_submission(self, challenge: Challenge, user: User, src_path: str):
        challenge_submission = {"challenge": challenge.id, "user": user.id, "src_path": src_path}
        serializer = ChallengeSubmissionSerializer(data=challenge_submission)
        serializer.is_valid(raise_exception=True)
        try:
            challenge_submission = serializer.save()
        except IntegrityError as e:
            return Response({"error": "This challenge is already completed"}, status=status.HTTP_400_BAD_REQUEST)
        return challenge_submission
