from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class VersionView(APIView):
    def get(self, request):
        return Response({"version": settings.VERSION}, status=status.HTTP_200_OK)
