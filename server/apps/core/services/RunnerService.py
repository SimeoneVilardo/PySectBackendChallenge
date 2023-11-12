from dataclasses import dataclass
import subprocess

@dataclass
class RunnerOutput:
    output: list
    errors: list

class RunnerService:
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
    def execute_with_input(cls, source_file: str, input_array = list()) -> RunnerOutput:
        process = subprocess.Popen(['python', source_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        input_string = '\n'.join(input_array)
        output, errors = process.communicate(input=input_string)
        output = list(filter(None, output.split('\n')))
        errors = list(filter(None, errors.split('\n')))
        result = RunnerOutput(output, errors)
        return result