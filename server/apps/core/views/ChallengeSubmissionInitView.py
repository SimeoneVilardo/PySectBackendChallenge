from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from server.apps.core.auth import SNSPermission
from server.apps.core.choices import ChallengeSubmissionStatusChoices
from server.apps.core.models import ChallengeSubmission
from server.apps.core.models.challenge import Challenge
from server.apps.core.serializers import NotificationSerializer
from server.apps.core.services.AwsLambdaService import AwsLambdaService
from server.apps.core.services.NotificationQueueService import NotificationQueueService


class ChallengeSubmissionInitView(generics.CreateAPIView):
    serializer_class = NotificationSerializer
    authentication_classes = []
    permission_classes = [SNSPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        message = serializer.validated_data.get("Message")
        challenge_submission_id = message.get("challenge_submission_id")
        if not challenge_submission_id:
            raise Exception("challenge_submission_id not found in message")
        challenge_submission = ChallengeSubmission.objects.select_related("challenge", "user").get(
            id=challenge_submission_id
        )
        try:
            lambda_response = self.create_lambda_function(challenge_submission)
            self.init_challenge_submission(challenge_submission, lambda_response["FunctionName"])
        except Exception as e:
            self.abort_challenge_submission(challenge_submission)
            return
        NotificationQueueService.publish(challenge_submission)

    def create_lambda_function(self, challenge_submission: ChallengeSubmission):
        challenge: Challenge = challenge_submission.challenge
        input_file = challenge.input
        src_data = AwsLambdaService.prepare_lambda_script(challenge_submission)
        is_valid_src_data = AwsLambdaService.validate_lambda_script(src_data)
        if not is_valid_src_data:
            raise Exception("Invalid src_data")
        zip_file = AwsLambdaService.create_zip(input_file, src_data)
        lambda_response = AwsLambdaService.create_lambda_function(f"submission_{challenge_submission.id}", zip_file)
        return lambda_response

    def abort_challenge_submission(self, challenge_submission: ChallengeSubmission):
        challenge_submission.status = ChallengeSubmissionStatusChoices.BROKEN
        challenge_submission.save()

    def init_challenge_submission(self, challenge_submission: ChallengeSubmission, function_name: str):
        challenge_submission.lambda_name = function_name
        challenge_submission.status = ChallengeSubmissionStatusChoices.READY
        challenge_submission.save()
