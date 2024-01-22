import ast
from django.core.files.base import File
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from server.apps.core.auth import CookieTokenAuthentication
from server.apps.core.models import Challenge, Submission
from server.apps.core.serializers import SubmissionSerializer
from server.apps.core.filters.SubmissionFilter import SubmissionFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

class SubmissionPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class SubmissionView(ListCreateAPIView, RetrieveAPIView):
    authentication_classes = (CookieTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Submission.objects.all()
    parser_classes = (MultiPartParser,)
    serializer_class = SubmissionSerializer
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubmissionFilter
    pagination_class = SubmissionPageNumberPagination

    def get_queryset(self):
        challenge_id = self.kwargs.get("challenge_id")
        qs = Submission.objects.filter(user=self.request.user, challenge_id=challenge_id)
        return qs

    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        challenge: Challenge = get_object_or_404(Challenge, id=kwargs["challenge_id"])
        file_obj: File = request.data.get("file")
        self.is_valid_python_file(file_obj)
        submission: Submission = self.create_submission(challenge, request.user, file_obj)
        serializer = self.get_serializer(submission)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def is_valid_python_file(self, file_obj: File):
        if not file_obj:
            raise serializers.ValidationError({"error": "No file received"})
        if file_obj.size == 0:
            raise serializers.ValidationError({"error": "Empty file"})
        if file_obj.size > 0.5 * 1024 * 1024:
            raise serializers.ValidationError({"error": "File size is too large (max 512 KB)"})
        if not file_obj.name.endswith(".py"):
            raise serializers.ValidationError({"error": "The file is not a Python file"})
        try:
            file_str = file_obj.read().decode("utf-8")
            file_obj.seek(0)
        except Exception as e:
            raise serializers.ValidationError({"error": "The file does not contain valid UTF-8 data"})
        try:
            ast.parse(file_str)
        except Exception as e:
            raise serializers.ValidationError({"error": "The file does not contain valid Python code"})
        return True

    def create_submission(self, challenge: Challenge, user: User, file_obj: File) -> Submission:
        submission = {"challenge": challenge.id, "user": user.id, "src_data": file_obj.read().decode("utf-8")}
        serializer = SubmissionSerializer(data=submission)
        serializer.is_valid(raise_exception=True)
        try:
            submission = serializer.save()
        except IntegrityError as e:
            raise serializers.ValidationError({"error": "Database integrity error"})
        return submission
