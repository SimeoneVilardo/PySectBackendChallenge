from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from server.apps.core.views.AuthView import AuthView
from server.apps.core.views.ChallengeSubmissionResultView import ChallengeSubmissionResultView
from server.apps.core.views.ChallengeSubmissionView import ChallengeSubmissionView
from server.apps.core.views.HealthView import HealthView
from server.apps.core.views.ChallengeSubmissionRunView import ChallengeSubmissionRunView
from server.apps.core.views.ChallengeView import ChallengeView
from server.apps.core.views.ChallengeSubmissionCreateView import ChallengeSubmissionCreateView
from server.apps.core.views.LoginView import LoginView
from server.apps.core.views.LogoutView import LogoutView
from server.common.views import create_dispatcher_view

urlpatterns = [
    path("health/", HealthView.as_view(), name="dummy_api"),
    path("me/", AuthView.as_view(), name="me_api"),
    path("login/", LoginView.as_view(), name="login_api"),
    path("logout/", LogoutView.as_view(), name="logout_api"),
    path("challenges/", ChallengeView.as_view(), name="challenge_list_api"),
    path("challenges/<int:id>/", ChallengeView.as_view(), name="challenge_retreive_api"),
    path(
        "challenge-submission/<int:id>/",
        create_dispatcher_view(
            {
                "GET": ChallengeSubmissionView,
                "POST": ChallengeSubmissionCreateView,
            }
        ),
        name="challenge_submission_api",
    ),
    path(
        "challenge-submission/<int:id>/run/", ChallengeSubmissionRunView.as_view(), name="challenge_submission_run_api"
    ),
    path(
        "challenge-submission/result/",
        ChallengeSubmissionResultView.as_view(),
        name="challenge_submission_result_api",
    ),
]
