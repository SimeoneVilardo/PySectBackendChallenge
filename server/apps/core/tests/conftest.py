from django.test import Client
import pytest

class CustomClient(Client):
    pass

@pytest.fixture
def django_client() -> CustomClient:
    return CustomClient()