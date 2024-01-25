from rest_framework import serializers
from server.apps.core.models.user import User


class UserSerializer(serializers.ModelSerializer):

    total_points = serializers.ReadOnlyField()
    used_points = serializers.ReadOnlyField()
    remaining_points = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ("id", "username", "email", "total_points", "used_points", "remaining_points")