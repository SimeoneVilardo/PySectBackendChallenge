import os
from django.conf import settings
from django.http import Http404
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.parsers import BaseParser
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from server.apps.core.choices import ChallengeSubmissionStatusChoices
from server.apps.core.models import ChallengeSubmission, Challenge
from server.apps.core.serializers import ChallengeSubmissionResultSerializer, ChallengeSubmissionSerializer
from server.apps.core.services.ChallengeSubmissionRunner import ChallengeSubmissionRunner
from server.apps.core.tasks.challenge_submission import check_submission_result


class PlainTextParser(BaseParser):
    media_type = "text/plain"

    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read()


class ChallengeSubmissionResultView(UpdateAPIView):
    parser_classes = [
        PlainTextParser,
    ]

    def post(self, request):
        print("Headers:", request.headers)
        print("Query parameters:", request.query_params)
        print("Body:", request.body)

        return Response(status=status.HTTP_201_CREATED)
