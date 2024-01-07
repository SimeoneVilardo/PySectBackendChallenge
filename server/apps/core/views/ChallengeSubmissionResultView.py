from django.http import Http404
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from server.apps.core.auth import SNSPermission
from server.apps.core.choices import ChallengeSubmissionStatusChoices
from server.apps.core.serializers import NotificationSerializer
from server.apps.core.models import ChallengeSubmission, Challenge
from server.apps.core.services.NotificationQueueService import NotificationQueueService


class ChallengeSubmissionResultView(CreateAPIView):
    serializer_class = NotificationSerializer
    authentication_classes = []
    permission_classes = [SNSPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        message = validated_data.get("Message")
        print(validated_data)

        challenge_submission_id = message["challenge_submission_id"]
        try:
            challenge_submission = ChallengeSubmission.objects.select_related("challenge", "user").get(
                id=challenge_submission_id
            )
        except ChallengeSubmission.DoesNotExist:
            raise Http404()
        if challenge_submission.status != ChallengeSubmissionStatusChoices.RUNNING:
            raise serializers.ValidationError({"error": "Challenge is not in RUNNING state"})

        challenge_submission.error = message["error"]
        challenge_submission.output = (
            message["output"].strip().replace("\r\n", "\n").replace("\r", "\n") if message["output"] else None
        )

        if challenge_submission.error:
            print(challenge_submission.error)
            challenge_submission.status = ChallengeSubmissionStatusChoices.FAILURE
            challenge_submission.save()
            NotificationQueueService.publish(challenge_submission)
            return

        challenge: Challenge = challenge_submission.challenge
        challenge_output = challenge.output.strip().replace("\r\n", "\n").replace("\r", "\n")
        challenge_submission.status = (
            ChallengeSubmissionStatusChoices.SUCCESS
            if challenge_output == challenge_submission.output
            else ChallengeSubmissionStatusChoices.FAILURE
        )
        print(challenge_output)
        print(challenge_submission.output)
        print(challenge_submission.status)
        challenge_submission.save()
        NotificationQueueService.publish(challenge_submission)
