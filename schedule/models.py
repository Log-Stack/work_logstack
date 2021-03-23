from django.contrib.auth.models import User
from django.db import models


class Schedule(models.Model):
    WORK_TYPES = ((1, 'work'), (2, 'vacation'),)
    # 근무, 휴가 ,(추가사항) 외근, ...
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    work_type = models.IntegerField(choices=WORK_TYPES)


class Schedule_permission(models.Model):
    permission_TYPES = ((1, 'waiting'), (2, 'approved'), (3, 'reject'),)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week_start_date = models.DateField()
    permission_TYPES = models.IntegerField(choices=permission_TYPES)
