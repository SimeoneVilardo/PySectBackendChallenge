import os
from django.conf import settings
from django.http import Http404
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.contrib.auth.models import User
from server.apps.core.choices import ChallengeSubmissionStatusChoices
from server.apps.core.models import ChallengeSubmission, Challenge


class ChallengeSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeSubmission
        fields = "__all__"


class ChallengeSubmissionRunView(UpdateAPIView):
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
        user_id = 1  # dummy user id
        user = User.objects.get(id=user_id)
        challenge_submission: ChallengeSubmission = self.get_object()
        challenge: Challenge = challenge_submission.challenge
        new_challenge_status = ChallengeSubmissionStatusChoices.SUCCESS

        update_data = {
            "status": new_challenge_status,
            "output_path": "output.txt",
            "error_path": "error.txt",
            "memory": 0,
            "time": 0,
        }
        serializer = self.get_serializer(challenge_submission, data=update_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
