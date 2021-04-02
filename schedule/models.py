from django.contrib.auth.models import User
from django.db import models

from authy.models import Profile


class Schedule(models.Model):
    WORK_TYPES = ((0, 'holiday'), (1, 'work'), (2, 'vacation'),)
    # 근무, 휴가 ,(추가사항) 외근, ...
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)
    work_type = models.IntegerField(choices=WORK_TYPES)

    # def __str__(self):
    #    user_profile = Profile.objects.get(user=self.user)
    #    result = user_profile.name
    #    if self.start is not None and self.end is not None:
    #        result += (" | " + self.date.strftime("%Y-%m-%d") + " | " + self.start.strftime("%H:%M") + " : " + self.end.strftime("%H:%M"))
    #    else:
    #        result += " | " + self.WORK_TYPES[self.work_type][1]
    #
    #    return result


class ScheduleApproved(models.Model):
    APPROVED_TYPES = ((1, 'waiting'), (2, 'approved'), (3, 'reject'),)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week_start_date = models.DateField()
    approved_type = models.IntegerField(choices=APPROVED_TYPES, default=1)
