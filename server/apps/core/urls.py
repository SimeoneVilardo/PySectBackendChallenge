from django.urls import path
from server.apps.core.views.ChallengeSubmissionRunView import ChallengeSubmissionRunView
from server.apps.core.views.ChallengeView import ChallengeView
from server.apps.core.views.ChallengeSubmissionCreateView import ChallengeSubmissionCreateView

urlpatterns = [
    path('challenge/<int:id>/', ChallengeView.as_view(), name='challenge_retreive_api'),
    path('challenge/', ChallengeView.as_view(), name='challenge_list_api'),
    path('challenge-submission/<int:id>/', ChallengeSubmissionCreateView.as_view(), name='challenge_submission_create_api'),
    path('challenge-submission/<int:id>/run/', ChallengeSubmissionRunView.as_view(), name='challenge_submission_run_api'),
]
