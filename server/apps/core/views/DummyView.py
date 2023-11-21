from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class DummyView(APIView):
    def get(self, request):
        data = {'message': 'Hello, this is a GET request!'}
        return Response(data, status=status.HTTP_200_OK)
