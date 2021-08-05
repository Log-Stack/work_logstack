from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Schedule(models.Model):
    WORK_TYPES = ((0, '휴일'), (1, '근무'), (2, '휴가'), (3, '반차'),)
    # 휴일, 근무, 휴가, 반차
    # 근무, 휴가 ,(추가사항) 외근, ...
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start = models.TimeField(null=True, default=None)
    end = models.TimeField(null=True, default=None)
    work_type = models.IntegerField(choices=WORK_TYPES, default=0)

    def __str__(self):
        result = str(self.user)
        if self.start is not None and self.end is not None:
            result += (" | " + self.date.strftime("%Y-%m-%d") + " | " + self.start.strftime(
                "%H:%M") + " : " + self.end.strftime("%H:%M"))
        else:
            result += " | " + self.WORK_TYPES[self.work_type][1]
        return result

    def schedule_created(sender, instance, *args, **kwargs):
        todo, todo_created = ToDo.objects.get_or_create(schedule=instance)
        todo.save()


class ScheduleApproved(models.Model):
    APPROVED_TYPES = ((1, 'waiting'), (2, 'approved'), (3, 'reject'),)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week_start_date = models.DateField()
    approved_type = models.IntegerField(choices=APPROVED_TYPES, default=1)


class ToDo(models.Model):
    schedule = models.OneToOneField(Schedule, on_delete=models.CASCADE)
    contents = models.TextField(default="작성된 ToDo가 없습니다")

    def __str__(self):
        return str(self.schedule.user) + " | " + self.schedule.date.strftime("%Y-%m-%d")


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    title = models.CharField(max_length=50)
    context = models.TextField(default="내용이 없습니다")

    def __str__(self):
        return str(self.user) + " | " + self.date.strftime("%Y-%m-%d") + " | " + self.title


post_save.connect(Schedule.schedule_created, sender=Schedule)
