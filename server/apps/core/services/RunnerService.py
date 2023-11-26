from dataclasses import dataclass
import json
import boto3
import zipfile
import io
import os
import time
import shutil
import uuid;

from server.apps.core.models import Challenge, ChallengeSubmission

@dataclass
class RunnerOutput:
    output: list
    error: str
    time: int
    memory: int

class RunnerService:

    runner_template_path : str = "runner-template/src.py.template"
    iam_client = boto3.client('iam')
    lambda_client = boto3.client('lambda', region_name="eu-north-1")

    @classmethod
    def create_random_id(cls) -> str:
        uuid_without_dash = str(uuid.uuid4()).replace('-', '')
        return uuid_without_dash

    @classmethod
    def add_script_to_zip(cls, zip_filename, src_file_str, input_str):
        with zipfile.ZipFile(zip_filename, 'a') as existing_zip:
            zip_info_src = zipfile.ZipInfo('src.py')
            zip_info_src.external_attr = 0o777 << 16  # Set file permission to "777"
            zip_info_input = zipfile.ZipInfo('input.txt')
            zip_info_input.external_attr = 0o777 << 16  # Set file permission to "777"
            existing_zip.writestr(zip_info_src, src_file_str)
            existing_zip.writestr(zip_info_input, input_str)

    @classmethod
    def create_lambda_function(cls, function_name, zip_file, role_name="PySectRunner", handler="src.lambda_handler", runtime="python3.11", memory_size=128, timeout=30):
        role = cls.iam_client.get_role(RoleName=role_name)
        response = cls.lambda_client.create_function(
            FunctionName=function_name,
            Runtime=runtime,
            Role=role['Role']['Arn'],
            Handler=handler,
            Code={
                'ZipFile': zip_file.read(),
            },
            MemorySize=memory_size,
            Timeout=timeout,
            Environment={
                'Variables': {
                    'PYSECT_BACKEND_API_KEY': 'xxx',
                }
            },
        )
        for i in range(30):
            response = cls.lambda_client.get_function(FunctionName=function_name)
            status = response['Configuration']['State']
            if status == 'Active':
                return response
            else:
                time.sleep(1)
        raise Exception("Error creating lambda function (timeout)")
    
    @classmethod
    def check_lambda_function_exists(cls, function_name):
        try:
            response = cls.lambda_client.get_function(FunctionName=function_name)
            return response
        except cls.lambda_client.exceptions.ResourceNotFoundException:
            return None

    @classmethod
    def check_lambda_function_is_active(cls, function_name):
        for i in range(30):
            response = cls.lambda_client.get_function(FunctionName=function_name)
            status = response['Configuration']['State']
            if status.lower() == 'active':
                return response
            else:
                time.sleep(1)
        raise Exception("Error creating lambda function (timeout)")
        
    
    @classmethod
    def invoke_lambda_function(cls, function_name, payload=dict()) -> RunnerOutput:
        response = cls.lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        response_payload = json.loads(response['Payload'].read().decode('utf-8'))
        if response_payload.get("statusCode") != 200:
            raise Exception("Error in lambda function")
        body = response_payload.get("body")
        out = body.get("stdout")
        out_lines = [line for line in out.split('\n') if line]
        err = body.get("stderr") if body.get("stderr") else None
        runner_output: RunnerOutput = RunnerOutput(output=out_lines, error=err, time=0, memory=0)
        return runner_output
    
    @classmethod
    def create_zip_file(cls, challenge_submission: ChallengeSubmission) -> io.BytesIO:
        template_path = os.path.join("server", "apps", "core", cls.runner_template_path)
        src_path = os.path.join("server", "apps", "core", "storage", "uploads", challenge_submission.src)
        input_path = os.path.join("server", "apps", "core", "storage", "inputs", challenge_submission.challenge.input_path)
        zip_package_template_path = os.path.join("server", "apps", "core", "runner-template", "package.zip.template")
        zip_package_path = os.path.join("server", "apps", "core", "runner-template", f"{cls.create_random_id()}.zip")

        shutil.copy(zip_package_template_path, zip_package_path)

        with open(template_path) as f:
            src_template = f.read()
        with open(src_path) as f:
            src = f.read()
        with open(input_path) as f:
            input = f.read()
        src_wrapped = src_template.replace('{{code}}', src)

        cls.add_script_to_zip(zip_package_path, src_wrapped, input)
        return open(zip_package_path, 'rb')