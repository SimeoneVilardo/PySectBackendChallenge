from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from server.apps.core.auth import CookieTokenAuthentication
from server.apps.core.models import ChallengeSubmission
from server.apps.core.serializers import ChallengeSubmissionSerializer


class ChallengeSubmissionView(RetrieveAPIView):
    authentication_classes = (CookieTokenAuthentication,)
    permission_classes = [IsAuthenticated]
    serializer_class = ChallengeSubmissionSerializer
    lookup_field = "id"

    def get_queryset(self):
        return ChallengeSubmission.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        challenge_submission = self.get_object()
        serializer = self.get_serializer(challenge_submission)
        return Response(serializer.data, status=status.HTTP_200_OK)
