from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import BaseParser
from rest_framework import serializers
import json
from rest_framework import generics
from server.apps.core.choices import ChallengeSubmissionStatusChoices
from rest_framework.parsers import JSONParser

from server.apps.core.models import ChallengeSubmission
from server.apps.core.models.challenge import Challenge
from server.apps.core.serializers import NotificationSerializer
from server.apps.core.services.ChallengeSubmissionRunner import ChallengeSubmissionRunner


class PlainTextParser(BaseParser):
    media_type = "text/plain"

    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read()


class ChallengeSubmissionInitView(APIView):
    parser_classes = [
        PlainTextParser,
    ]

    def post(self, request):
        print("Headers:", request.headers)
        print("Query parameters:", request.query_params)
        print("Body:", request.body)
        return Response(status=status.HTTP_201_CREATED)
