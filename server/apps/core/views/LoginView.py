import ast
from django.core.files.base import File
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from server.apps.core.choices import ChallengeSubmissionStatusChoices
from server.apps.core.models import Challenge, ChallengeSubmission
from server.apps.core.serializers import ChallengeSubmissionSerializer
from server.apps.core.services.ChallengeSubmissionRunner import ChallengeSubmissionRunner
from server.apps.core.tasks.challenge_submission import create_lambda_function


class LoginView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_201_CREATED)
