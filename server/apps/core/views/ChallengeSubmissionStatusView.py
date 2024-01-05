# serializers.py
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from server.apps.core.models import Challenge, ChallengeSubmission
from server.apps.core.serializers import ChallengeSubmissionStatusSerializer


class ChallengeSubmissionStatusView(RetrieveAPIView):
    permission_classes = [HasAPIKey]
    queryset = ChallengeSubmission.objects.all()
    serializer_class = ChallengeSubmissionStatusSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        challenge_submission = self.get_object()
        serializer = self.get_serializer(challenge_submission)
        return Response(serializer.data, status=status.HTTP_200_OK)
