from celery import shared_task
from server.apps.core.choices import ChallengeSubmissionStatusChoices

from server.apps.core.models import Challenge, ChallengeSubmission
from server.apps.core.services.ChallengeSubmissionRunner import ChallengeSubmissionRunner


def create_zip_file(challenge: Challenge, challenge_submission: ChallengeSubmission):
    if challenge_submission.src_data is None:
        raise Exception("No src_data found in challenge submission")
    src_data = challenge_submission.src_data
    with open("server/apps/core/lambda/lambda_function.py", "r") as file:
        template = file.read()
    src_data = template.replace("###SRC###", src_data)
    input_file = challenge.input
    zip_file = ChallengeSubmissionRunner.create_zip(input_file, src_data)
    return zip_file


def init_challenge_submission(challenge_submission: ChallengeSubmission, function_name: str):
    challenge_submission.lambda_name = function_name
    challenge_submission.status = ChallengeSubmissionStatusChoices.READY
    challenge_submission.save()


@shared_task
def create_lambda_function(challenge_submission_id: int):
    challenge_submission = ChallengeSubmission.objects.select_related("challenge").get(id=challenge_submission_id)
    challenge: Challenge = challenge_submission.challenge
    try:
        zip_file = create_zip_file(challenge, challenge_submission)
        lambda_response = ChallengeSubmissionRunner.create_lambda_function(
            f"submission_{challenge_submission.id}", zip_file
        )
        init_challenge_submission(challenge_submission, lambda_response["FunctionName"])
    except Exception as e:
        challenge_submission.status = ChallengeSubmissionStatusChoices.BROKEN
        challenge_submission.save()


@shared_task
def check_submission_result(challenge_submission_id: int):
    challenge_submission = ChallengeSubmission.objects.select_related("challenge").get(id=challenge_submission_id)
    challenge: Challenge = challenge_submission.challenge
    output = challenge.output.strip().replace("\r\n", "\n").replace("\r", "\n")
    challenge_submission.status = (
        ChallengeSubmissionStatusChoices.SUCCESS
        if output == challenge_submission.output
        else ChallengeSubmissionStatusChoices.FAILURE
    )
    challenge_submission.save()
