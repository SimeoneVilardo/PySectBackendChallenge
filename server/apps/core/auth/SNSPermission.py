from rest_framework.permissions import BasePermission
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography import x509
import requests
import re
import base64
from urllib.parse import urlparse

cache = dict()


class SNSPermission(BasePermission):
    default_host_pattern = re.compile(r"^sns\.[a-zA-Z0-9\-]{3,}\.amazonaws\.com(\.cn)?$")

    def has_permission(self, request, view):
        return self.validate_url(request.data["SigningCertURL"]) and self.verify_sns_data(request.data)

    def validate_url(self, url_to_validate, host_pattern=None):
        if host_pattern is None:
            host_pattern = self.default_host_pattern
        parsed = urlparse(url_to_validate)
        return (
            parsed.scheme == "https" and parsed.path.endswith(".pem") and host_pattern.match(parsed.netloc) is not None
        )

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
