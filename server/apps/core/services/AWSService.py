from django.conf import settings
from server.apps.core.models import Challenge, ChallengeSubmission
import boto3


class AWSService:
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    s3 = boto3.client("s3")

    @classmethod
    def download(cls, path: str):
        return cls.s3.get_object(Bucket=cls.bucket_name, Key=path)["Body"].read()

    @classmethod
    def download_src(cls, challenge_submission: ChallengeSubmission):
        return cls.download(challenge_submission.src_path)

    @classmethod
    def download_input(cls, challenge: Challenge):
        return cls.download(challenge.input_path)

    @classmethod
    def download_output(cls, challenge: Challenge):
        return cls.download(challenge.output_path)
