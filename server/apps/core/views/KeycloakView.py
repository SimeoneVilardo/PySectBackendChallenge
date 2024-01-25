# views.py

from keycloak import KeycloakOpenID
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import OAuth2Authentication

keycloak_openid = KeycloakOpenID(server_url="http://localhost:9004/auth/",
                                client_id="pysect",
                                realm_name="pysect")

class KeycloakView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Your view logic here
        return Response({"message": "Authenticated"})
