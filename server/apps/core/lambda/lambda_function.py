import builtins
import sys
import json
from io import StringIO
import urllib.request
import traceback
import boto3

with open("input.json") as input_file:
    parsed_input_list = json.load(input_file)
parsed_input = []


def fake_input(prompt=""):
    try:
        return parsed_input.pop(0)
    except IndexError:
        raise EOFError("No more input")


builtins.input = fake_input


def notify_result(challenge_submission_id, output=None, error=None):
    data = {"output": output, "error": error, "challenge_submission_id": challenge_submission_id}
    sns = boto3.client("sns", region_name="eu-north-1")
    sns.publish(
        TopicArn="arn:aws:sns:eu-north-1:340650704585:challenge-submission-result",
        Message=json.dumps(data),
    )


###SRC###


def lambda_handler(event, context):
    challenge_submission_id = event["id"]
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
    notify_result(challenge_submission_id, output, error)
