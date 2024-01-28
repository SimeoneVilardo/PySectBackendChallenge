from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        cookie_response = Response(status=status.HTTP_204_NO_CONTENT)
        cookie_response.delete_cookie(key="token")
        return cookie_response
