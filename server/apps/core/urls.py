from django.urls import path
from server.apps.core.views.AuthView import AuthView
from server.apps.core.views.SubmissionResultView import SubmissionResultView
from server.apps.core.views.SubmissionView import SubmissionView
from server.apps.core.views.HealthView import HealthView
from server.apps.core.views.SubmissionRunView import SubmissionRunView
from server.apps.core.views.ChallengeView import ChallengeView
from server.apps.core.views.LoginView import LoginView
from server.apps.core.views.LogoutView import LogoutView
from server.apps.core.views.VersionView import VersionView
from server.common.views import create_dispatcher_view

urlpatterns = [
    # Utils
    path("health/", HealthView.as_view(), name="dummy_api"),
    path("version/", VersionView.as_view(), name="version_api"),
    # Auth
    path("me/", AuthView.as_view(), name="me_api"),
    path("login/", LoginView.as_view(), name="login_api"),
    path("logout/", LogoutView.as_view(), name="logout_api"),
    # Challenges
    path("challenges/", ChallengeView.as_view(), name="challenges_api"),
    path("challenges/<int:id>/", ChallengeView.as_view(), name="challenge_api"),
    # Submissions
    path(
        "challenges/<int:challenge_id>/submissions/",
        SubmissionView.as_view(),
        name="submissions_api",
    ),
    path(
        "challenges/<int:challenge_id>/submissions/<int:id>/",
        SubmissionView.as_view(),
        name="submission_api",
    ),
    path(
        "challenges/submissions/<int:id>/run/",
        SubmissionRunView.as_view(),
        name="submissions_run_api",
    ),
    path(
        "challenge-submission/result/",
        SubmissionResultView.as_view(),
        name="submissions_result_api",
    ),
]
