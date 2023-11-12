import subprocess
from rest_framework.generics import RetrieveAPIView
from rest_framework import serializers
from rest_framework.response import Response
from server.apps.core.models.challenge import Challenge

from server.apps.core.services.RunnerService import RunnerOutput, RunnerService

class RunnerOutputSerializer(serializers.Serializer):
    output = serializers.ListField(read_only=True)
    errors = serializers.ListField(read_only=True)

class RunnerView(RetrieveAPIView):
    serializer_class = RunnerOutputSerializer
    queryset = Challenge.objects.all()

    def retrieve(self, request, *args, **kwargs):
        challenge = self.get_object()
        input_path = 'server/apps/core/inputs'
        program_path = 'server/apps/core/uploads'

        challenge_input = f"{input_path}/{challenge.input_path}"
        challenge_src = f"{program_path}/{challenge.src_path}"
        input_array = RunnerService.read_input(challenge_input)
        result : RunnerOutput = RunnerService.execute_with_input(challenge_src, input_array)
        serializer = self.get_serializer(result)
        serialized_data = serializer.data
        return Response(serialized_data)