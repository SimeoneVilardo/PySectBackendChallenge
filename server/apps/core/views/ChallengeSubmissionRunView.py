from django.conf import settings
from django.http import Http404
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from server.apps.core.choices import ChallengeSubmissionStatusChoices

from server.apps.core.models import ChallengeSubmission, ChallengeInput, Challenge, User
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
        try:
            challenge_submission = ChallengeSubmission.objects.select_related('challenge').prefetch_related('challenge__challenge_inputs').get(id=self.kwargs['id'])
        except ChallengeSubmission.DoesNotExist:
            raise Http404()
        if challenge_submission.status != ChallengeSubmissionStatusChoices.READY:
            raise serializers.ValidationError({"error": "Challenge submission is already run"})
        return challenge_submission

    def partial_update(self, request, *args, **kwargs):
        user_id = 1 # dummy user id
        user = User.objects.get(id=user_id)
        challenge_submission : ChallengeSubmission = self.get_object()
        challenge : Challenge = challenge_submission.challenge
        challenge_inputs : list(ChallengeInput) = challenge.challenge_inputs.all()

        #for challenge_input in challenge_inputs: TODO: run all inputs
        challenge_input = challenge_inputs[0]
        zip_file = RunnerService.create_zip_file(challenge_input, challenge_submission)
        lambda_function_name = f"user_{user.name}__challenge_{challenge.name}__submission_{str(challenge_submission.id)}"
        lambda_function = RunnerService.check_lambda_function_exists(lambda_function_name)
        if lambda_function is None:
            lambda_function = RunnerService.create_lambda_function(lambda_function_name, zip_file)
        challenge_response: RunnerOutput = RunnerService.invoke_lambda_function(lambda_function_name)

        challenge_output = self.get_challenge_output(challenge_input)
        success = challenge_response.output == challenge_output
        new_challenge_status = ChallengeSubmissionStatusChoices.SUCCESS if success else ChallengeSubmissionStatusChoices.FAILURE

        update_data = {"status": new_challenge_status, "output": challenge_response.output, "error": challenge_response.error, "memory": challenge_response.memory, "time": challenge_response.time}
        serializer = self.get_serializer(challenge_submission, data=update_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_challenge_output(cls, challenge_input: ChallengeInput):
        challenge_output_path = f"{settings.BASE_OUTPUT_PATH}/{challenge_input.output}"
        with open(challenge_output_path) as f:
            challenge_output = f.readlines()
        return challenge_output