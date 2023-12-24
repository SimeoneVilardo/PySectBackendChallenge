import builtins
import sys
import json
from io import StringIO
import urllib.request
import traceback

with open("input.json") as input_file:
    parsed_input_list = json.load(input_file)
parsed_input = []


def fake_input(prompt=""):
    try:
        return parsed_input.pop(0)
    except IndexError:
        raise EOFError("No more input")


builtins.input = fake_input


def make_patch_request(url, data):
    try:
        parts = url.split("/")
        host = parts[2]
        json_data = json.dumps(data).encode("utf-8")
        headers = {
            "Content-type": "application/json",
            "Host": host,
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "User-Agent": "pysect-lambda",
        }
        request = urllib.request.Request(url, data=json_data, method="PATCH", headers=headers)
        with urllib.request.urlopen(request) as response:
            status_code = response.getcode()
            return status_code
    except urllib.error.HTTPError as e:
        return e.code
    except urllib.error.URLError as e:
        return None


def notify_result(challenge_id, output=None, error=None):
    url = f"https://api.pysect.letz.dev/api/challenge-submission/{challenge_id}/result/"
    data = {"output": output, "error": error}
    make_patch_request(url, data)


###SRC###


def lambda_handler(event, context):
    challenge_id = event["id"]
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
    notify_result(challenge_id, output, error)
