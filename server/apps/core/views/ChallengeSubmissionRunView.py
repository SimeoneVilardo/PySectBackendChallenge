from django.conf import settings
from django.http import Http404
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from server.apps.core.auth import CookieTokenAuthentication
from server.apps.core.choices import ChallengeSubmissionStatusChoices
from server.apps.core.models import ChallengeSubmission
from server.apps.core.serializers import ChallengeSubmissionSerializer
from server.apps.core.services.AwsStepFunctionService import AwsStepFunctionService


class ChallengeSubmissionRunView(UpdateAPIView):
    authentication_classes = (CookieTokenAuthentication,)
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
        input_payload = self.create_input_payload(challenge_submission)
        sfn_name = f"challenge-submission-{challenge_submission.id}-{settings.DJANGO_ENV}"
        response = AwsStepFunctionService.invoke_step_function(sfn_name, input_payload)
        challenge_submission.status = ChallengeSubmissionStatusChoices.RUNNING
        challenge_submission.save()
        serializer = self.get_serializer(challenge_submission)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def create_input_payload(self, challenge_submission: ChallengeSubmission):
        payload = {}
        payload["id"] = challenge_submission.id
        payload["src"] = challenge_submission.src_data
        payload["input"] = challenge_submission.challenge.input
        return payload
