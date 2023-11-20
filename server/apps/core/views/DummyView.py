from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import boto3


class DummyView(APIView):
    def get(self, request):
        iam_client = boto3.client('iam')

        try:
            role = iam_client.create_role(
                RoleName="PySectRunner",
                AssumeRolePolicyDocument='''{
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Effect": "Allow",
                        "Principal": {"Service": "lambda.amazonaws.com"},
                        "Action": "sts:AssumeRole"
                    }]
                }'''
            )
        except iam_client.exceptions.EntityAlreadyExistsException:
            # Se il ruolo esiste già, otteniamolo
            role = iam_client.get_role(RoleName=role_name)

        function_name = "YourFunctionName"  # Sostituisci con il nome desiderato per la Lambda Function
        role_name = "YourRoleName"  # Sostituisci con il nome desiderato per il ruolo IAM
        handler = "src.lambda_handler"  # Sostituisci con il nome del tuo gestore di eventi Lambda
        runtime = "python3.11"  # Sostituisci con la versione di Python desiderata

        self.create_lambda_function(function_name, role_name, handler, runtime)
        data = {'message': 'Hello, this is a GET request!'}
        return Response(data, status=status.HTTP_200_OK)
