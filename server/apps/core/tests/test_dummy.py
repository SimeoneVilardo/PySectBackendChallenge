from rest_framework import status
import pytest


class TestDummy:
    def test_dummy(self, django_client):
        response = django_client.get(f"/api/dummy/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Hello, this is a GET request!"}
