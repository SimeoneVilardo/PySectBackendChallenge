# views.py

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers

class UploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class UploadView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        serializer = UploadSerializer(data=request.data)
        base_path = "server/apps/core/uploads"

        if serializer.is_valid():
            # Handle the uploaded file here (e.g., save it to disk, process it)
            uploaded_file = serializer.validated_data['file']

            # Add your file handling logic here
            with open(f"{base_path}/{uploaded_file.name}", 'wb') as file:
                file.write(uploaded_file.file.getvalue())

            return Response({'status': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
