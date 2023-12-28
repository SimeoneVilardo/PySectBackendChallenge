import os
from django.conf import settings
from django.http import Http404
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from server.apps.core.choices import ChallengeSubmissionStatusChoices
from server.apps.core.models import ChallengeSubmission, Challenge
from server.apps.core.serializers import ChallengeSubmissionResultSerializer, ChallengeSubmissionSerializer
from server.apps.core.services.ChallengeSubmissionRunner import ChallengeSubmissionRunner
from server.apps.core.tasks.challenge_submission import check_submission_result


class ChallengeSubmissionResultView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChallengeSubmissionResultSerializer

    def partial_update(self, request, *args, **kwargs):
        print("request.data", request.data)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            print("e.detail", e.detail)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        challenge_submission_id = validated_data["challenge_submission_id"]
        try:
            challenge_submission = ChallengeSubmission.objects.select_related("challenge").get(
                id=challenge_submission_id
            )
        except ChallengeSubmission.DoesNotExist:
            raise Http404()
        if challenge_submission.status != ChallengeSubmissionStatusChoices.RUNNING:
            raise serializers.ValidationError({"error": "Challenge is not in RUNNING state"})

        challenge_submission.error = validated_data["error"]
        challenge_submission.output = (
            validated_data["output"].strip().replace("\r\n", "\n").replace("\r", "\n")
            if validated_data["output"]
            else None
        )

        if challenge_submission.error:
            challenge_submission.status = ChallengeSubmissionStatusChoices.FAILURE
            challenge_submission.save()
            return Response(status=status.HTTP_200_OK)

        challenge: Challenge = challenge_submission.challenge
        challenge_output = challenge.output.strip().replace("\r\n", "\n").replace("\r", "\n")
        challenge_submission.status = (
            ChallengeSubmissionStatusChoices.SUCCESS
            if challenge_output == challenge_submission.output
            else ChallengeSubmissionStatusChoices.FAILURE
        )
        challenge_submission.save()
        return Response(status=status.HTTP_200_OK)
