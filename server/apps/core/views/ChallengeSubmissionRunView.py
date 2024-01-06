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
from server.apps.core.serializers import ChallengeSubmissionSerializer
from server.apps.core.services.ChallengeSubmissionRunner import ChallengeSubmissionRunner


class ChallengeSubmissionRunView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = ChallengeSubmission.objects.all()
    lookup_field = "id"
    serializer_class = ChallengeSubmissionSerializer

    def get_object(self):
        try:
            challenge_submission = ChallengeSubmission.objects.select_related("challenge").get(id=self.kwargs["id"])
        except ChallengeSubmission.DoesNotExist:
            raise Http404()
        if challenge_submission.status != ChallengeSubmissionStatusChoices.READY:
            raise serializers.ValidationError({"error": "Challenge is not in READY state"})
        return challenge_submission

    def partial_update(self, request, *args, **kwargs):
        challenge_submission: ChallengeSubmission = self.get_object()
        challenge: Challenge = challenge_submission.challenge

        response = ChallengeSubmissionRunner.invoke_lambda_function(
            challenge_submission.lambda_name, payload={"id": challenge_submission.id}
        )
        challenge_submission.status = ChallengeSubmissionStatusChoices.RUNNING
        challenge_submission.save()
        serializer = self.get_serializer(challenge_submission)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
