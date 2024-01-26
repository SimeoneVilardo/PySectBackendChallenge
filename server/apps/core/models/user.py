from django.contrib import auth
from django.db.models import Sum
from server.apps.core.choices import SubmissionStatusChoices

class User(auth.models.AbstractUser):

    @property
    def total_points(self):
        from server.apps.core.models import Submission, Challenge
        completed_challenges = Submission.objects.filter(user=self, status=SubmissionStatusChoices.SUCCESS).values('challenge')
        total_points = Challenge.objects.filter(id__in=completed_challenges).aggregate(Sum('points'))['points__sum']
        return total_points if total_points else 0

    @property
    def used_points(self):
        used_points = self.redeemed_rewards.aggregate(total=Sum('price'))['total']
        return used_points if used_points else 0

    @property
    def remaining_points(self):
        return self.total_points - self.used_points
