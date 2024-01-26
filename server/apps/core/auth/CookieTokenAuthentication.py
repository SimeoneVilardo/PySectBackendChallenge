from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from server.apps.core.models.user import User


class CookieTokenAuthentication(TokenAuthentication):
    """
    Custom token authentication using a cookie.
    """

    def authenticate(self, request):
        token = request.COOKIES.get("token")

        if not token:
            raise AuthenticationFailed("No token provided")

        token_obj = self.get_model().objects.filter(key=token).first()

        if not token_obj:
            raise AuthenticationFailed("Invalid token")

        return (token_obj.user, token)
