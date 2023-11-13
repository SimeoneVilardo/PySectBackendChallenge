from dataclasses import dataclass
import subprocess
import os

@dataclass
class RunnerOutput:
    output: list
    error: list

class RunnerService:
    env = os.environ.copy()
    env["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"

    @classmethod
    def read_input(cls, input_path):
        try:
            with open(input_path, 'r') as file:
                lines = file.readlines()
                lines = [line.rstrip('\n') for line in lines]
                return lines
        except FileNotFoundError:
            print(f"File {input_path} not found")
            return []
        
    @classmethod
    def read_output(cls, output_path):
        try:
            with open(output_path, 'r') as file:
                lines = file.readlines()
                lines = [line.rstrip('\n') for line in lines]
                return lines
        except FileNotFoundError:
            print(f"File {output_path} not found")
            return []

    @classmethod
    def execute_with_input(cls, source_file: str, input_array = list()) -> RunnerOutput:
        process = subprocess.Popen(['python', source_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=cls.env)
        input_string = '\n'.join(input_array)
        output, error = process.communicate(input=input_string)
        output = list(filter(None, output.split('\n')))
        error = list(filter(None, error.split('\n')))
        result = RunnerOutput(output, error)
        return result