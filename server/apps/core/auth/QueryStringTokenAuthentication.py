from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class QueryStringTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.query_params.get("token")
        if token:
            return self.authenticate_credentials(token)
        else:
            msg = "No token provided."
            raise AuthenticationFailed(msg)
