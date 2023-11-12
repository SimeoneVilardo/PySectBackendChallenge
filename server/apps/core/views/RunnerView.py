import subprocess
from rest_framework.generics import RetrieveAPIView
from rest_framework import serializers
from rest_framework.response import Response

from server.apps.core.services.RunnerService import RunnerOutput, RunnerService

class RunnerOutputSerializer(serializers.Serializer):
    output = serializers.ListField(read_only=True)
    errors = serializers.ListField(read_only=True)

class RunnerView(RetrieveAPIView):
    serializer_class = RunnerOutputSerializer

    def get(self, request):
        input_path = 'server/apps/core/inputs/sum.txt'
        program_path = 'server/apps/core/uploads/sum.py'
        input_array = RunnerService.read_input(input_path)
        result : RunnerOutput = RunnerService.execute_with_input(program_path, input_array)
        serializer = self.get_serializer(result)
        serialized_data = serializer.data
        return Response(serialized_data)    