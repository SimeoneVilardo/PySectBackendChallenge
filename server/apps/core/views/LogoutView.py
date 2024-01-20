from rest_framework.views import APIView
from rest_framework.response import Response


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        cookie_response = Response()
        cookie_response.delete_cookie(key="token")
        return cookie_response
