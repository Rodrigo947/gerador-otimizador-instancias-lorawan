
import os

import boto3
from botocore.exceptions import ClientError
from rest_framework.response import Response
from rest_framework.views import APIView


class Email(APIView):
  def __init__(self):
    self.AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    self.AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    self.AWS_REGION = os.environ.get("AWS_REGION")
    self.EMAIL = os.environ.get("EMAIL")

  def post(self, request):
    name = request.data['name']
    email = request.data['email']
    company_name = request.data['company_name']
    msg = request.data['msg']

    subject = f'Nova Lead | {company_name}'
    body = f'Novo contato de {name} da empresa {company_name}.\n\n \
        Email: {email}\n\n \
        Mensagem: {msg}'

    ses_client = boto3.client(
        service_name='ses',
        aws_access_key_id=self.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
        region_name=self.AWS_REGION
    )

    email = {
        'Source': self.EMAIL,
        'Destination': {'ToAddresses': [self.EMAIL]},
        'Message': {
            'Subject': {'Data': subject},
            'Body': {'Text': {'Data': body}}
        }
    }

    try:
      ses_client.send_email(**email)
      return Response({'message': 'Email sent successfully.'})
    except ClientError as e:
      return Response({'message': 'Failed to send email.'}, status=500)
