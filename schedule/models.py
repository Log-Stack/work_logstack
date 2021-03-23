from django.contrib.auth.models import User
from django.db import models

from authy.models import Profile


class Schedule(models.Model):
    WORK_TYPES = ((1, 'work'), (2, 'vacation'),)
    # 근무, 휴가 ,(추가사항) 외근, ...
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    work_type = models.IntegerField(choices=WORK_TYPES)

    def __str__(self):
        user_profile = Profile.objects.get(user=self.user)
        return user_profile.team.name + " - " + user_profile.name + " | " + self.start.strftime(
            "%H:%M") + " : " + self.end.strftime("%H:%M")


class ScheduleApproved(models.Model):
    APPROVED_TYPES = ((1, 'waiting'), (2, 'approved'), (3, 'reject'),)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week_start_date = models.DateField()
    approved_type = models.IntegerField(choices=APPROVED_TYPES)
