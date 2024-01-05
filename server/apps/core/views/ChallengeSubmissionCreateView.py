import ast
from django.core.files.base import File
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from server.apps.core.choices import ChallengeSubmissionStatusChoices
from server.apps.core.models import Challenge, ChallengeSubmission
from server.apps.core.serializers import ChallengeSubmissionSerializer
from server.apps.core.services.ChallengeSubmissionRunner import ChallengeSubmissionRunner
import boto3
import json


class ChallengeSubmissionCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = ChallengeSubmission.objects.all()
    parser_classes = (MultiPartParser,)
    serializer_class = ChallengeSubmissionSerializer

    def post(self, request, *args, **kwargs):
        challenge: Challenge = get_object_or_404(Challenge, id=kwargs["id"])

        file_obj: File = request.data.get("file")
        self.is_valid_python_file(file_obj)

        challenge_submission: ChallengeSubmission = self.create_challenge_submission(
            challenge, request.auth.user, file_obj
        )

        # Publish message to SNS topic
        sns = boto3.client("sns", region_name="eu-north-1")
        sns.publish(
            TopicArn="arn:aws:sns:eu-north-1:340650704585:challenge-submission-create",
            Message=json.dumps({"challenge_submission_id": challenge_submission.id}),
        )

        serializer = self.get_serializer(challenge_submission)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def is_valid_python_file(self, file_obj: File):
        if not file_obj:
            raise serializers.ValidationError({"error": "No file received"})
        if file_obj.size == 0:
            raise serializers.ValidationError({"error": "Empty file"})
        if file_obj.size > 0.5 * 1024 * 1024:
            raise serializers.ValidationError({"error": "File size is too large (max 512 KB)"})
        if not file_obj.name.endswith(".py"):
            raise serializers.ValidationError({"error": "The file is not a Python file"})
        try:
            ast.parse(file_obj.read().decode())
            file_obj.seek(0)
        except SyntaxError:
            raise serializers.ValidationError({"error": "The file does not contain valid Python code"})
        return True

    def create_challenge_submission(self, challenge: Challenge, user: User, file_obj: File) -> ChallengeSubmission:
        challenge_submission = {"challenge": challenge.id, "user": user.id, "src_data": file_obj.read().decode("utf-8")}
        serializer = ChallengeSubmissionSerializer(data=challenge_submission)
        serializer.is_valid(raise_exception=True)
        try:
            challenge_submission = serializer.save()
        except IntegrityError as e:
            raise serializers.ValidationError({"error": "Database integrity error"})
        return challenge_submission

    def update_challenge_submission(self, challenge_submission: ChallengeSubmission, function_name: str):
        challenge_submission.lambda_name = function_name
        challenge_submission.status = ChallengeSubmissionStatusChoices.READY
        challenge_submission.save()
