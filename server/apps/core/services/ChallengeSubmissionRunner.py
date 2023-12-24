import time
import io
import zipfile
import boto3
import json
from django.conf import settings


class ChallengeSubmissionRunner:
    lambda_client = boto3.client("lambda")
    ecr_client = boto3.client("ecr")
    iam_client = boto3.client("iam")

    @classmethod
    def create_zip(cls, input_file, src_file):
        in_memory_zip = io.BytesIO()
        with zipfile.ZipFile(in_memory_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zipf:
            zipf.writestr("input.json", input_file)
            zipf.writestr("lambda_function.py", src_file)
        in_memory_zip.seek(0)
        return in_memory_zip

    @classmethod
    def create_lambda_function(
        cls,
        function_name,
        zip_file,
        role_name="PySectRunner",
        handler="lambda_function.lambda_handler",
        runtime="python3.11",
        memory_size=128,
        timeout=30,
    ):
        role = cls.iam_client.get_role(RoleName=role_name)
        response = cls.lambda_client.create_function(
            FunctionName=function_name,
            Runtime=runtime,
            Role=role["Role"]["Arn"],
            Handler=handler,
            Code={
                "ZipFile": zip_file.read(),
            },
            MemorySize=memory_size,
            Timeout=timeout,
            Environment={
                "Variables": {
                    "PYSECT_BACKEND_API_KEY": "xxx",
                }
            },
        )
        return response

    @classmethod
    def invoke_lambda_function(cls, function_name, payload=dict()):
        response = cls.lambda_client.invoke(
            FunctionName=function_name, InvocationType="Event", Payload=json.dumps(payload)
        )
        return response
