from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class NotificationView(APIView):
    def post(self, request):
        print("POST request:")
        print("Headers:", request.headers)
        print("Body:", request.data)
        print("Query parameters:", request.query_params)
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        print("GET request:")
        print("Headers:", request.headers)
        print("Body:", request.data)
        print("Query parameters:", request.query_params)
        return Response(status=status.HTTP_200_OK)
