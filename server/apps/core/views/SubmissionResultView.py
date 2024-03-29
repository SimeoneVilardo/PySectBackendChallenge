from django.http import Http404
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from server.apps.core.auth import SNSPermission
from server.apps.core.choices import SubmissionStatusChoices
from server.apps.core.serializers import NotificationSerializer
from server.apps.core.models import Submission, Challenge
from server.apps.core.services.NotificationQueueService import NotificationQueueService


class SubmissionResultView(CreateAPIView):
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

        submission_id = message["challenge_submission_id"]
        try:
            submission = Submission.objects.select_related("challenge", "user").get(id=submission_id)
        except Submission.DoesNotExist:
            raise Http404()
        if submission.status != SubmissionStatusChoices.RUNNING:
            raise serializers.ValidationError({"error": "Challenge is not in RUNNING state"})

        submission.error = message["error"]
        submission.output = (
            message["output"].strip().replace("\r\n", "\n").replace("\r", "\n") if message["output"] else None
        )

        if submission.error:
            submission.status = SubmissionStatusChoices.FAILURE
            submission.save()
            NotificationQueueService.publish(submission)
            return

        challenge: Challenge = submission.challenge
        challenge_output = challenge.output.strip().replace("\r\n", "\n").replace("\r", "\n")
        if challenge_output == submission.output:
            submission.status = SubmissionStatusChoices.SUCCESS
        else:
            submission.status = SubmissionStatusChoices.FAILURE
            submission.error = "Output did not match"
        submission.save()
        NotificationQueueService.publish(submission)
