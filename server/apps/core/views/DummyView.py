from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import docker
import subprocess


class DummyView(APIView):
    def get(self, request):
        self.run_docker(
            'server/apps/core/storage/uploads/sum.py',
            'server/apps/core/storage/inputs/sum_1.txt',
            'server/apps/core/storage/user_outputs/docker_sum_stdout.txt',
            'server/apps/core/storage/user_outputs/docker_sum_stderr .txt'
        )
        data = {'message': 'Hello, this is a GET request!'}
        return Response(data, status=status.HTTP_200_OK)

    def run_docker(self, src_path, input_txt_path, output_txt_path, error_txt_path):
        container_name = "pysect-runner"
        docker_image = "arm64v8/python:3.11-bullseye"

        docker_client = docker.from_env()
        docker_client.containers.run(
            image=docker_image,
            detach=True,
            name=container_name,
            stdin_open=True,
            tty=True,
        )

        subprocess.run(f"docker exec -i {container_name} bash -c \"mkdir /code\"", shell=True)
        subprocess.run(f"docker exec -i {container_name} bash -c \"mkdir /out\"", shell=True)
        subprocess.run(f"docker cp {src_path} {container_name}:/code/app.py", shell=True)
        subprocess.run(f"docker cp {input_txt_path} {container_name}:/code/stdin.txt", shell=True)
        subprocess.run(f"docker exec -i {container_name} bash -c \"python /code/app.py < /code/stdin.txt > /out/stdout.txt 2> /out/stderr.txt\"", shell=True)
        subprocess.run(f"docker cp {container_name}:/out/stdout.txt {output_txt_path}", shell=True)
        subprocess.run(f"docker cp {container_name}:/out/stderr.txt {error_txt_path}", shell=True)

        docker_client.containers.get(container_name).remove(force=True)