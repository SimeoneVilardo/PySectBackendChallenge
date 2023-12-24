import ast
from django.core.files.base import File
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from server.apps.core.choices import ChallengeSubmissionStatusChoices
from server.apps.core.models import Challenge, ChallengeSubmission
from server.apps.core.serializers import ChallengeSubmissionSerializer
from server.apps.core.services.ChallengeSubmissionRunner import ChallengeSubmissionRunner


class ChallengeSubmissionCreateView(generics.CreateAPIView):
    queryset = ChallengeSubmission.objects.all()
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        user_id = 1  # dummy user id

        user: User = User.objects.get(id=user_id)
        challenge: Challenge = get_object_or_404(Challenge, id=kwargs["id"])

        file_obj: File = request.data.get("file")
        self.is_valid_python_file(file_obj)

        challenge_submission: ChallengeSubmission = self.create_challenge_submission(challenge, user, file_obj)

        # TODO: move this to an async task

        zip_file = self.create_zip_file(challenge, challenge_submission)
        lambda_response = ChallengeSubmissionRunner.create_lambda_function(
            f"submission_{challenge_submission.id}", zip_file
        )

        self.update_challenge_submission(challenge_submission, lambda_response["FunctionName"])
        return Response(status=status.HTTP_201_CREATED)

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

    def create_zip_file(self, challenge: Challenge, challenge_submission: ChallengeSubmission):
        if challenge_submission.src_data is None:
            raise serializers.ValidationError({"error": "No source code found"})
        src_data = challenge_submission.src_data
        with open("server/apps/core/lambda/lambda_function.py", "r") as file:
            template = file.read()
        src_data = template.replace("###SRC###", src_data)
        input_file = challenge.input
        zip_file = ChallengeSubmissionRunner.create_zip(input_file, src_data)
        return zip_file

    def update_challenge_submission(self, challenge_submission: ChallengeSubmission, function_name: str):
        challenge_submission.lambda_name = function_name
        challenge_submission.status = ChallengeSubmissionStatusChoices.READY
        challenge_submission.save()
