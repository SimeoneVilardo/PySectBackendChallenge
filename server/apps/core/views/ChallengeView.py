# serializers.py
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from server.apps.core.models import Challenge, ChallengeSubmission

class ChallengeSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeSubmission
        fields = '__all__'


class ChallengeSerializer(serializers.ModelSerializer):
    challenge_submissions = ChallengeSubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = Challenge
        exclude = ['input_path', 'output_path'] 

class ChallengeView(GenericAPIView, ListModelMixin, RetrieveModelMixin):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)