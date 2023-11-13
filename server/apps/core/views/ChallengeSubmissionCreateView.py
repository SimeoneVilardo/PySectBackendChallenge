from django.conf import settings
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from server.apps.core.models import User, Challenge, ChallengeSubmission

class ChallengeSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeSubmission
        fields = '__all__'

class ChallengeSubmissionFileSerializer(serializers.Serializer):
    file = serializers.FileField()

class ChallengeSubmissionCreateView(generics.CreateAPIView):
    serializer_class = ChallengeSubmissionFileSerializer
    parser_classes = (FileUploadParser,)
    queryset = ChallengeSubmission.objects.all()

    def post(self, request, *args, **kwargs):
        file_obj = request.data.get('file')
        user_id = 1 # dummy user id

        if not file_obj:
            return Response({'error': 'No file received'}, status=status.HTTP_400_BAD_REQUEST)
        
        challenge = Challenge.objects.get(id=kwargs['id'])
        user = User.objects.get(id=user_id)
        challenge_submission = {"challenge": challenge.id, "user": user.id, "src": file_obj.name}
        serializer = ChallengeSubmissionSerializer(data=challenge_submission)
        serializer.is_valid(raise_exception=True)
        try:
            challenge_submission = serializer.save()
        except IntegrityError as e:
            return Response({'error': 'This challenge is already completed'}, status=status.HTTP_400_BAD_REQUEST)
        src_path = f"{settings.BASE_SRC_PATH}/{challenge_submission.src}"
        with open(src_path, 'wb+') as file:
            for chunk in file_obj.chunks():
                file.write(chunk)

        return Response({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)