from django.conf import settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data.get("token")
        if token is not None:
            cookie_response = Response()
            secure = not settings.DEBUG
            max_age = 60 * 60 * 24 * 30  # 30 days
            cookie_response.set_cookie(
                key="token", value=token, httponly=True, secure=secure, samesite="Strict", max_age=max_age
            )
            return cookie_response
        return Response(status=status.HTTP_200_OK)
