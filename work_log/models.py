import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class WorkHour(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(blank=True, null=True)

    @property
    def endTime(self):
        end_time = self.end_time + datetime.timedelta(minutes=5)
        return datetime.datetime(
            end_time.year, end_time.month, end_time.day, end_time.hour, 30 * (end_time.minute // 30))\
            .strftime("%H:%M")

    @property
    def startTime(self):
        start_time = self.start_time + datetime.timedelta(minutes=20)
        return datetime.datetime(
            start_time.year, start_time.month, start_time.day, start_time.hour, 30 * (start_time.minute // 30))\
            .strftime("%H:%M")


class WorkLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField(default=False)
