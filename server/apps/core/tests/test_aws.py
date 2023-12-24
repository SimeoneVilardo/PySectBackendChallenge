from rest_framework import status
import pytest
from server.apps.core.services.AWSService import AWSService

from server.apps.core.services.ChallengeSubmissionRunner import ChallengeSubmissionRunner


class TestAws:
    def test_aws(self):
        aws_service = AWSService()
        pass
