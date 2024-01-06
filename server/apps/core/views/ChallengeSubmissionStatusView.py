from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from server.apps.core.auth import CookieTokenAuthentication
from server.apps.core.models import ChallengeSubmission
from server.apps.core.serializers import ChallengeSubmissionStatusSerializer


class ChallengeSubmissionStatusView(RetrieveAPIView):
    authentication_classes = (CookieTokenAuthentication,)
    permission_classes = [IsAuthenticated]
    queryset = ChallengeSubmission.objects.all()
    serializer_class = ChallengeSubmissionStatusSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        challenge_submission = self.get_object()
        serializer = self.get_serializer(challenge_submission)
        return Response(serializer.data, status=status.HTTP_200_OK)
