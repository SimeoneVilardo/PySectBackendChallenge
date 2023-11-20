from dataclasses import dataclass
import os
import boto3
import zipfile
import io

from server.apps.core.models import Challenge, ChallengeSubmission, ChallengeInput

@dataclass
class RunnerOutput:
    output: list
    error: list

class RunnerService:
    @classmethod
    def create_lambda_function(cls, function_name, zip_file, region="eu-north-1", role_name="PySectRunner", handler="src.lambda_handler", runtime="python3.11", memory_size=128, timeout=30):
        iam_client = boto3.client('iam')
        role = iam_client.get_role(RoleName=role_name)
        lambda_client = boto3.client('lambda', region_name=region)
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime=runtime,
            Role=role['Role']['Arn'],
            Handler=handler,
            Code={
                'ZipFile': zip_file.read(),
            },
            MemorySize=memory_size,
            Timeout=timeout,
        )
        return response
    
    @classmethod
    def create_zip_file(cls, challenge_input: ChallengeInput, challenge_submission: ChallengeSubmission):
        challenge: Challenge = challenge_submission.challenge
        with open('src.py.template') as f:
            src_template = f.read()
        with open(challenge_submission.src) as f:
            src = f.read()
        with open(challenge_input.input) as f:
            input = f.read()
        src_wrapped = src_template.replace('{{code}}', src)
        zip_contents = io.BytesIO()
        with zipfile.ZipFile(f"{challenge.name}.zip", 'w') as zip_file:
            zip_file.writestr('src.py', src_wrapped)
            zip_file.writestr('input.txt', input)
        zip_contents.seek(0)
        return zip_contents