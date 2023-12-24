import builtins
import sys
import json
from io import StringIO
import http.client

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
    parts = url.split("/")
    host = parts[2]
    path = "/" + "/".join(parts[3:])
    connection = http.client.HTTPConnection(host)
    headers = {"Content-type": "application/json"}
    connection.request("PATCH", path, body=data, headers=headers)
    response = connection.getresponse()
    # response_data = response.read().decode("utf-8")
    # print(response_data)
    connection.close()


def notify_result(challenge_id, output, error):
    url = f"http://37.182.11.36/api/challenge-submission/{challenge_id}/result/"
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
        except Exception as e:
            error = str(e)
            break

    output = sys.stdout.getvalue().encode("utf-8")
    sys.stdout = original_stdout
    notify_result(challenge_id, output, error)
