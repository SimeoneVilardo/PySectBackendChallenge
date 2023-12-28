from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers
from rest_framework.parsers import BaseParser


class PlainTextParser(BaseParser):
    media_type = "text/plain"

    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read()


class NotificationView(APIView):
    parser_classes = [
        parsers.JSONParser,
        parsers.FormParser,
        parsers.MultiPartParser,
        PlainTextParser,
    ]

    def post(self, request):
        print("POST request:")
        print("Headers:", request.headers)
        print("Body:", request.data)
        print("Query parameters:", request.query_params)
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        print("GET request:")
        print("Headers:", request.headers)
        print("Body:", request.data)
        print("Query parameters:", request.query_params)
        return Response(status=status.HTTP_200_OK)
