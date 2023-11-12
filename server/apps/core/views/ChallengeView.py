# serializers.py
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from server.apps.core.models import Challenge, ChallengeInput

class ChallengeInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeInput
        fields = ('id', 'name', 'files')

class ChallengeSerializer(serializers.ModelSerializer):
    challenge_inputs = ChallengeInputSerializer(many=True)

    class Meta:
        model = Challenge
        fields = ('id', 'name', 'reward', 'challenge_inputs')

    def create(self, validated_data):
        inputs_data = validated_data.pop('challenge_inputs')
        challenge = Challenge.objects.create(**validated_data)
        for input_data in inputs_data:
            ChallengeInput.objects.create(challenge=challenge, **input_data)
        return challenge

class ChallengeView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ChallengeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)