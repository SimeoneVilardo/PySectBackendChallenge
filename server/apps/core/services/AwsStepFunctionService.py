import boto3
import json
from django.conf import settings


class AwsStepFunctionService:
    sfn_client = boto3.client("stepfunctions")

    @classmethod
    def invoke_step_function(cls, name, payload = dict()):
        input_text = json.dumps(payload)
        response = cls.sfn_client.start_execution(
            stateMachineArn=settings.AWS_CHALLENGE_SUBMISSION_RUN_STEP_FUNCTION_ARN,
            name=name,
            input=input_text,
            # traceHeader='string'
        )
        return response
