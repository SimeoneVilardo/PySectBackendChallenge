from rest_framework import status
import pytest

class TestChallenge:
    def test_get_challenges(self, django_client):
        response = django_client.get(f'/api/challenge/')
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'data': 'Hello World!'}