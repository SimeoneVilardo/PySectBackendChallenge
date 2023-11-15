from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import docker
import subprocess
from server.apps.core.tasks import add


class DummyView(APIView):
    def get(self, request):
        result = add.delay(4, 4)
        r = result.ready()
        somma = result.get(timeout=1)
        # Your logic for handling GET requests

        self.run_docker(
            'server/apps/core/storage/uploads/sum.py',
            'server/apps/core/storage/inputs/sum_1.txt',
            'server/apps/core/storage/user_outputs/docker_sum.txt'
        )
        data = {'message': 'Hello, this is a GET request!'}
        return Response(data, status=status.HTTP_200_OK)

    def run_docker(self, file_python_path, file_txt_input_path, file_txt_output_path):
        container_name = "pysect-runner"
        docker_image = "python:3.8"

        docker_client = docker.from_env()
        docker_client.containers.run(
            image=docker_image,
            detach=True,
            name=container_name,
            stdin_open=True,
            tty=True,
        )

        subprocess.run(f"docker exec -i {container_name} bash -c \"mkdir /code\"", shell=True)
        subprocess.run(f"docker cp {file_python_path} {container_name}:/code/app.py", shell=True)
        subprocess.run(f"docker cp {file_txt_input_path} {container_name}:/code/input.txt", shell=True)
        subprocess.run(f"docker exec -i {container_name} bash -c \"python /code/app.py < /code/input.txt > /code/output.txt\"", shell=True)
        subprocess.run(f"docker stats --no-stream {container_name} --format \"{{.MemUsage}}\"", shell=True)
        subprocess.run(f"docker cp {container_name}:/code/output.txt {file_txt_output_path}", shell=True)

        docker_client.containers.get(container_name).remove(force=True)