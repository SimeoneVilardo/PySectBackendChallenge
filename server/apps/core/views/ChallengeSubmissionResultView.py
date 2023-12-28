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
    queryset = ChallengeSubmission.objects.all()
    serializer_class = ChallengeSubmissionResultSerializer
    lookup_field = "id"

    def get_object(self):
        try:
            challenge_submission = ChallengeSubmission.objects.get(id=self.kwargs["id"])
        except ChallengeSubmission.DoesNotExist:
            raise Http404()
        if challenge_submission.status != ChallengeSubmissionStatusChoices.RUNNING:
            raise serializers.ValidationError({"error": "Challenge is not in RUNNING state"})
        return challenge_submission

    def partial_update(self, request, *args, **kwargs):
        user_id = 1  # dummy user id
        user = User.objects.get(id=user_id)

        print("request.data", request.data)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            print("e.detail", e.detail)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        validated_data = serializer.validated_data

        challenge_submission: ChallengeSubmission = self.get_object()
        challenge_submission.output = (
            validated_data["output"].strip().replace("\r\n", "\n").replace("\r", "\n")
            if validated_data["output"]
            else None
        )
        challenge_submission.error = validated_data["error"]
        challenge_submission.save()

        check_submission_result.delay(challenge_submission.id)
        return Response(status=status.HTTP_200_OK)
