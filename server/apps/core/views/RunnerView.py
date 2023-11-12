from django.conf import settings
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework import serializers
from rest_framework.response import Response
from server.apps.core.models import Challenge, ChallengeResult, ChallengeInput

from server.apps.core.services.RunnerService import RunnerOutput, RunnerService

class RunnerOutputSerializer(serializers.Serializer):
    challenge_id = serializers.IntegerField()
    output = serializers.ListField()
    error = serializers.ListField()
    
    def create(self, validated_data):
        return ChallengeResult.objects.create(**validated_data)

class RunnerView(CreateAPIView):
    serializer_class = RunnerOutputSerializer
    queryset = ChallengeResult.objects.all()

    def get_object(self):
        challenge_input = ChallengeInput.objects.select_related('challenge').get(
            challenge_id=self.kwargs['challenge_id'],
            pk=self.kwargs['input_id']
        )
        return challenge_input

    def create(self, request, *args, **kwargs):
        challenge_input = self.get_object()
        challenge = challenge_input.challenge
        src_path = f"{settings.BASE_SRC_PATH}/{challenge.src}"
        results = []
        for input_file in challenge_input.files:
            input_path = f"{settings.BASE_INPUT_PATH}/{input_file}"
            input_array = RunnerService.read_input(input_path)
            result : RunnerOutput = RunnerService.execute_with_input(src_path, input_array)
            results.append({"challenge_id":challenge.id, "output": result.output, "error": result.error})
        serializer = self.get_serializer(data=results, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)