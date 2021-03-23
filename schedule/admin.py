from django.contrib import admin

# Register your models here.
from schedule.models import Schedule, ScheduleApproved

admin.site.register(Schedule)
admin.site.register(ScheduleApproved)