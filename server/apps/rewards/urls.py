from django.urls import path

from server.apps.rewards.views.RewardsView import RewardsView

urlpatterns = [
    # Utils
    path("", RewardsView.as_view(), name="rewards_api"),
    path("<int:id>/", RewardsView.as_view(), name="reward_api"),

]
