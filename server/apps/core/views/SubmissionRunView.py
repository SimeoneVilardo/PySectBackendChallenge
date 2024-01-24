from django.conf import settings
from django.http import Http404
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from server.apps.core.auth import CookieTokenAuthentication
from server.apps.core.choices import SubmissionStatusChoices
from server.apps.core.models import Submission
from server.apps.core.serializers import SubmissionSerializer
from server.apps.core.services.AwsStepFunctionService import AwsStepFunctionService
from server.apps.core.services.NotificationQueueService import NotificationQueueService


class SubmissionRunView(UpdateAPIView):
    authentication_classes = (CookieTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Submission.objects.all()
    lookup_field = "id"
    serializer_class = SubmissionSerializer

    def get_object(self):
        try:
            submission = Submission.objects.select_related("challenge").get(id=self.kwargs["id"])
        except Submission.DoesNotExist:
            raise Http404()
        if submission.status != SubmissionStatusChoices.READY:
            raise serializers.ValidationError({"error": "Challenge is not in READY state"})
        return submission

    def partial_update(self, request, *args, **kwargs):
        submission: Submission = self.get_object()
        input_payload = self.create_input_payload(submission)
        sfn_name = f"submission-{submission.id}-{settings.DJANGO_ENV}"
        response = AwsStepFunctionService.invoke_step_function(sfn_name, input_payload)
        submission.status = SubmissionStatusChoices.RUNNING
        submission.save()
        serializer = self.get_serializer(submission)
        NotificationQueueService.publish(submission)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def create_input_payload(self, submission: Submission):
        payload = {}
        payload["id"] = submission.id
        payload["src"] = submission.src_data
        payload["input"] = submission.challenge.input
        return payload
