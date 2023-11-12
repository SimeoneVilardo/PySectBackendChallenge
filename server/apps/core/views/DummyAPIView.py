from rest_framework.views import APIView
from rest_framework.response import Response

class DummyAPIView(APIView):
    def get(self, request):
        return Response({'data': 'Hello World!'})