import time
from django.conf import settings
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from server.apps.core.choices import ChallengeSubmissionStatusChoices

from server.apps.core.models import ChallengeSubmission, ChallengeInput, Challenge
from server.apps.core.services.RunnerService import RunnerOutput, RunnerService

class ChallengeSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeSubmission
        fields = '__all__'

class ChallengeSubmissionRunView(UpdateAPIView):
    queryset = ChallengeSubmission.objects.all()
    lookup_field = 'id'
    serializer_class = ChallengeSubmissionSerializer

    def get_object(self):
        challenge_submission = ChallengeSubmission.objects.select_related('challenge').prefetch_related('challenge__challenge_inputs').get(challenge_id=self.kwargs['id'])
        return challenge_submission

    def partial_update(self, request, *args, **kwargs):
        challenge_submission : ChallengeSubmission = self.get_object()
        challenge : Challenge = challenge_submission.challenge
        challenge_inputs : list(ChallengeInput) = challenge.challenge_inputs.all()
        src_path = f"{settings.BASE_SRC_PATH}/{challenge_submission.src}"

        user_error_path_array = []
        user_output_path_array = []

        success = True
        for challenge_input in challenge_inputs:
            input_path = f"{settings.BASE_INPUT_PATH}/{challenge_input.input}"
            output_path = f"{settings.BASE_OUTPUT_PATH}/{challenge_input.output}"
            input_array = RunnerService.read_input(input_path)
            user_output_array = RunnerService.read_output(output_path)
            run : RunnerOutput = RunnerService.execute_with_input(src_path, input_array)

            user_output_name = f"{challenge.name}_{str(challenge_input.id)}_output_{str(int(time.time()))}.txt"
            user_error_name = f"{challenge.name}_{str(challenge_input.id)}_error_{str(int(time.time()))}.txt"
            user_output_path = f"{settings.BASE_USER_OUTPUT_PATH}/{user_output_name}"
            user_error_path = f"{settings.BASE_USER_OUTPUT_PATH}/{user_error_name}"
            user_error_path_array.append(user_error_path)
            user_output_path_array.append(user_output_path)

            with open(user_output_path, 'w') as file:
                for user_output_line in user_output_array:
                    file.write(f"{user_output_line}\n")
            with open(user_error_path, 'w') as file:
                for user_error_line in run.error:
                    file.write(f"{user_error_line}\n")
            if success is True and run.output != user_output_array:
                success = False

        new_challenge_status = ChallengeSubmissionStatusChoices.SUCCESS if success else ChallengeSubmissionStatusChoices.FAILURE
        update_data = {"status": new_challenge_status, "output": user_output_path_array, "error": user_error_path_array, "memory": 1, "time": 1}
        serializer = self.get_serializer(challenge_submission, data=update_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
