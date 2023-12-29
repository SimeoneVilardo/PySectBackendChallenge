import asyncio
from typing import AsyncGenerator
from django.http import StreamingHttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.renderers import BaseRenderer
import boto3
from server.apps.core.auth import QueryStringTokenAuthentication
from server.apps.core.services.QueueService import QueueService

sqs = boto3.resource("sqs", region_name="eu-north-1")


class ServerSentEventRenderer(BaseRenderer):
    media_type = "text/event-stream"
    format = "txt"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class ChallengeSubmissionStatus(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [QueryStringTokenAuthentication]
    renderer_classes = [JSONRenderer, ServerSentEventRenderer]

    def get(self, request):
        generator = QueueService.status_consumer(request.auth.user)
        response = StreamingHttpResponse(streaming_content=generator, content_type="text/event-stream")
        response["X-Accel-Buffering"] = "no"  # Disable buffering in nginx
        response["Cache-Control"] = "no-cache"  # Ensure clients don't cache the data
        return response
