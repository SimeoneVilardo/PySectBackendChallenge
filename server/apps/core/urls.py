from django.urls import path
from server.apps.core.views.ChallengeView import ChallengeView
from server.apps.core.views.RunnerView import RunnerView

from server.apps.core.views.DummyAPIView import DummyAPIView
from server.apps.core.views.UploadView import UploadView

urlpatterns = [
    path('dummy/', DummyAPIView.as_view(), name='dummy_api'),
    path('upload/', UploadView.as_view(), name='upload_api'),
    path('run/<int:pk>/', RunnerView.as_view(), name='run_api'),
    path('challenge/', ChallengeView.as_view(), name='challenge_api'),
]
