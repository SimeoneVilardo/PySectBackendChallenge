import builtins
import sys
import json
import traceback
import boto3
import os
from io import StringIO

with open("input.json") as input_file:
    parsed_input_list = json.load(input_file)
parsed_input = []


def fake_input(prompt=""):
    try:
        return parsed_input.pop(0)
    except IndexError:
        raise EOFError("No more input")


builtins.input = fake_input


def notify_result(output=None, error=None):
    topic_arn = os.environ.get("AWS_CHALLENGE_SUBMISSION_RESULT_TOPIC_ARN")
    region_name = os.environ.get("AWS_REGION")
    challenge_submission_id = os.environ.get("CHALLENGE_SUBMISSION_ID")
    data = {"output": output, "error": error, "challenge_submission_id": challenge_submission_id}
    sns = boto3.client("sns", region_name=region_name)
    sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps(data),
    )


###SRC###


def lambda_handler(event, context):
    original_stdout = sys.stdout
    sys.stdout = StringIO()
    error = None

    while len(parsed_input_list) > 0:
        global parsed_input
        parsed_input = parsed_input_list.pop(0)
        try:
            # start custom code
            main()
            # end custom code
        except:
            error = traceback.format_exc()
            break

    output = sys.stdout.getvalue()
    if not output:
        output = None
    sys.stdout = original_stdout
    notify_result(output, error)
