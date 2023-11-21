from datetime import datetime
import os
from django.conf import settings
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework import generics
from rest_framework.response import Response
from django.core.files.uploadedfile import InMemoryUploadedFile
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

        submission_folder = self.create_submission_directory(user_id, challenge.id)
        src_path = self.create_src_path(submission_folder)

        challenge_submission = self.create_challenge_submission(challenge, user, src_path)
        
        self.save_src_file(challenge_submission, file_obj, submission_folder)
        return Response({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)
    
    def create_challenge_submission(self, challenge: Challenge, user: User, src_path: str):
        challenge_submission = {"challenge": challenge.id, "user": user.id, "src": src_path}
        serializer = ChallengeSubmissionSerializer(data=challenge_submission)
        serializer.is_valid(raise_exception=True)
        try:
            challenge_submission = serializer.save()
        except IntegrityError as e:
            return Response({'error': 'This challenge is already completed'}, status=status.HTTP_400_BAD_REQUEST)
        return challenge_submission

    def save_src_file(self, challenge_submission: ChallengeSubmission, file_obj: InMemoryUploadedFile, submission_folder: str):
        src_full_path = f"{settings.BASE_SRC_PATH}/{challenge_submission.src}"
        with open(src_full_path, 'wb+') as file:
            for chunk in file_obj.chunks():
                file.write(chunk)

    def create_src_path(self, submission_folder: str):
        timestamp = datetime.now().strftime("%Y_%m_%d__%H_%M_%S_%f")
        src_path = f"{submission_folder}/{timestamp}.py"
        return src_path

    def create_submission_directory(self, user_id: int, challenge_id: int):
        user_folder = f"user_{str(user_id)}"
        self.create_directory(f"{settings.BASE_SRC_PATH}/{user_folder}")
        challenge_folder = f"challenge_{str(challenge_id)}"
        self.create_directory(f"{settings.BASE_SRC_PATH}/{user_folder}/{challenge_folder}")
        return f"user_{str(user_id)}/challenge_{str(challenge_id)}"

    def create_directory(self, directory_path: str):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Directory '{directory_path}' created successfully.")
        else:
            print(f"Directory '{directory_path}' already exists.")
