from django.urls import path

from server.apps.core.views.DummyAPIView import DummyAPIView

urlpatterns = [
    path('dummy/', DummyAPIView.as_view(), name='dummy_api'),
]
