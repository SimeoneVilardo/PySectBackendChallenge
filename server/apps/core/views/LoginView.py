from django.conf import settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        except Exception as e:
            raise AuthenticationFailed("Invalid credentials")
        token = response.data.get("token")
        if token is None:
            raise AuthenticationFailed("Invalid credentials")
        cookie_response = Response()
        secure = not settings.DEBUG
        max_age = 60 * 60 * 24 * 30  # 30 days
        cookie_response.set_cookie(
            key="token", value=token, httponly=True, secure=secure, samesite="Strict", max_age=max_age
        )
        return cookie_response
