from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import BaseParser
import json
from server.apps.core.choices import ChallengeSubmissionStatusChoices

from server.apps.core.models import ChallengeSubmission
from server.apps.core.models.challenge import Challenge
from server.apps.core.services.ChallengeSubmissionRunner import ChallengeSubmissionRunner


class NotificationView(APIView):
    def post(self, request):
        raw_body = request.body
        print(request.headers)
        print(raw_body)
        body = json.loads(raw_body)
        message = body.get("Message")
        if not message:
            raise Exception("Message not found in body")
        message = json.loads(message)
        challenge_submission_id = message.get("challenge_submission_id")
        if not challenge_submission_id:
            raise Exception("challenge_submission_id not found in message")
        self.create_lambda_function(challenge_submission_id)
        return Response(status=status.HTTP_201_CREATED)

    def create_zip_file(self, challenge: Challenge, challenge_submission: ChallengeSubmission):
        if challenge_submission.src_data is None:
            raise Exception("No src_data found in challenge submission")
        src_data = challenge_submission.src_data
        with open("server/apps/core/lambda/lambda_function.py", "r") as file:
            template = file.read()
        src_data = template.replace("###SRC###", src_data)
        input_file = challenge.input
        zip_file = ChallengeSubmissionRunner.create_zip(input_file, src_data)
        return zip_file

    def init_challenge_submission(self, challenge_submission: ChallengeSubmission, function_name: str):
        challenge_submission.lambda_name = function_name
        challenge_submission.status = ChallengeSubmissionStatusChoices.READY
        challenge_submission.save()

    def create_lambda_function(self, challenge_submission_id: int):
        challenge_submission = ChallengeSubmission.objects.select_related("challenge").get(id=challenge_submission_id)
        challenge: Challenge = challenge_submission.challenge
        try:
            zip_file = self.create_zip_file(challenge, challenge_submission)
            lambda_response = ChallengeSubmissionRunner.create_lambda_function(
                f"submission_{challenge_submission.id}", zip_file
            )
            self.init_challenge_submission(challenge_submission, lambda_response["FunctionName"])
        except Exception as e:
            challenge_submission.status = ChallengeSubmissionStatusChoices.BROKEN
            challenge_submission.save()
