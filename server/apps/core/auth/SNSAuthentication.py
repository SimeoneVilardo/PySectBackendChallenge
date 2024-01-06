from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography import x509
import requests

cache = dict()


class SNSAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if not self.verify_sns_data(request.data):
            raise AuthenticationFailed("Invalid SNS message")
        return ("AWS_SNS", "AWS_SNS")

    def verify_sns_data(self, messagePayload):
        if messagePayload["SignatureVersion"] != "1":
            return False
        messagePayload["TopicArn"] = messagePayload["TopicArn"].replace(" ", "")
        signatureFields = self.get_fields_by_message_type(messagePayload["Type"])
        strToSign = self.get_payload_to_verify(messagePayload, signatureFields)
        certStr = self.get_cert(messagePayload)
        certificateSNS = x509.load_pem_x509_certificate(certStr.text.encode(), default_backend())
        public_keySNS = certificateSNS.public_key()
        decoded_signature = base64.b64decode(messagePayload["Signature"])
        try:
            public_keySNS.verify(decoded_signature, strToSign.encode(), padding.PKCS1v15(), hashes.SHA1())
            return True
        except Exception as e:
            print("Signature could not be verified")
            return False

    # Obtain the fields for signature based on message type.
    def get_fields_by_message_type(self, type):
        if type == "SubscriptionConfirmation" or type == "UnsubscribeConfirmation":
            return ["Message", "MessageId", "SubscribeURL", "Timestamp", "Token", "TopicArn", "Type"]
        elif type == "Notification":
            return ["Message", "MessageId", "Subject", "Timestamp", "TopicArn", "Type"]
        else:
            return []

    # Create the string to sign.
    def get_payload_to_verify(self, messagePayload, signatureFields):
        signatureStr = ""
        for key in signatureFields:
            if key in messagePayload:
                signatureStr += key + "\n" + messagePayload[key] + "\n"
        return signatureStr

    # **** Certificate Fetching ****
    # Certificate caching
    def get_cert_from_server(self, url):
        response = requests.get(url)
        return response

    def get_cert_from_cache(self, url):
        if url not in cache:
            cache[url] = self.get_cert_from_server(url)
        return cache[url]

    def get_cert(self, messagePayload):
        certLoc = messagePayload["SigningCertURL"].replace(" ", "")
        responseCert = self.get_cert_from_cache(certLoc)
        return responseCert
