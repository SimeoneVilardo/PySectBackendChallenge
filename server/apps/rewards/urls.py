from django.urls import path
from server.apps.rewards.views.RedemptionView import RedemptionView
from server.apps.rewards.views.RewardsView import RewardsView

urlpatterns = [
    # Utils
    path("", RewardsView.as_view(), name="rewards_api"),
    path("<int:id>/", RewardsView.as_view(), name="reward_api"),
    path("<int:id>/redeem/", RedemptionView.as_view(), name="redeem_api"),
    path("redemptions/", RedemptionView.as_view(), name="redemptions_api"),

]
