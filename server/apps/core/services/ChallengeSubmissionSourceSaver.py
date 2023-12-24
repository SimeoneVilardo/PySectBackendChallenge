from abc import ABC, abstractmethod
import uuid
import boto3
from django.conf import settings
from server.apps.core.models import Challenge, ChallengeSubmission


class ChallengeSubmissionSourceSaver(ABC):
    @abstractmethod
    def save(self, challenge_source, filename) -> str:
        pass


class BucketChallengeSubmissionSourceSaver(ChallengeSubmissionSourceSaver):
    def __init__(self):
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        self.s3 = boto3.client("s3")

    def save(self, file_obj) -> str:
        filename = f"submissions/{uuid.uuid4()}.py"
        file_obj.seek(0)
        self.s3.upload_fileobj(file_obj, self.bucket_name, filename)
        return filename


class FakeChallengeSubmissionSourceSaver(ChallengeSubmissionSourceSaver):
    def save(self, challenge_source, filename) -> str:
        pass
