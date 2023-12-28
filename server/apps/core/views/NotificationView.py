from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import BaseParser
import json


class PlainTextParser(BaseParser):
    media_type = "text/plain"

    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read()


class NotificationView(APIView):
    parser_classes = [
        PlainTextParser,
    ]

    def post(self, request):
        print("Headers:", request.headers)
        print("Query parameters:", request.query_params)
        try:
            body = json.loads(request.body)
            message = body.get("Message")
            if not message:
                raise Exception("Message not found in body")
            message = json.loads(message)
            challenge_submission_id = message.get("challenge_submission_id")
            if not challenge_submission_id:
                raise Exception("challenge_submission_id not found in message")
            print("challenge_submission_id:", challenge_submission_id)
        except Exception as e:
            print("Error:", str(e))

        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        print("GET request:")
        print("Headers:", request.headers)
        print("Body:", request.data)
        print("Query parameters:", request.query_params)
        return Response(status=status.HTTP_200_OK)
