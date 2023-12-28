from rest_framework import serializers
import json

"""
Example of data received from SNS:
{
    "Type": "Notification",
    "MessageId": "a8c54162-4634-5c60-84da-1f65b75ebd09",
    "TopicArn": "arn:aws:sns:eu-north-1:340650704585:challenge-submission-create",
    "Message": "{\"challenge_submission_id\": 24}",
    "Timestamp": "2023-12-28T21:56:58.675Z",
    "SignatureVersion": "1",
    "Signature": "ITV0M2ZiJW3TAQ+k3QwfY+R2owjNG5XaFq7DP49M79Zg4YC9VkO6McieVL/leUCpPAiM6aYt8qt5HU0QTnQCflJFA/23phAr93J+kZIapfjd5rgnGPuiBylVAB+PNEDuT3HBqrTNQ11Gl7MZIXCnoFBeYtmcVt8hJCrkTMiKEW+ma/rVK4eqwkBYvlXpL4CRzH5MP2TXZvdKTsq7L7OnAdTA5NNIxWj/HDtmXE6G5TERjsIG/Dd4+qpIo6IaW+HQoE43U6d9Zw7Q6xlCQBxnIqQIiFFGk9w9a2VZXunoO+qHjZ+LEmUH6cCRf9DihbtI9ks9UkLOuC9MMDToeQlCww==",
    "SigningCertURL": "https://sns.eu-north-1.amazonaws.com/SimpleNotificationService-01d088a6f77103d0fe307c0069e40ed6.pem",
    "UnsubscribeURL": "https://sns.eu-north-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-north-1:340650704585:challenge-submission-create:fa2e07c4-bee4-43e1-bda9-5c798990c1ad"
}
"""


class JSONStringField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            return json.loads(data)
        except ValueError:
            raise serializers.ValidationError("Invalid JSON")


class NotificationSerializer(serializers.Serializer):
    Type = serializers.CharField()
    MessageId = serializers.CharField()
    TopicArn = serializers.CharField()
    Message = JSONStringField()
    Timestamp = serializers.CharField()
    SignatureVersion = serializers.CharField()
    Signature = serializers.CharField()
    SigningCertURL = serializers.CharField()
    UnsubscribeURL = serializers.CharField()
