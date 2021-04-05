from django.contrib import admin

# Register your models here.
from .models import Schedule, ScheduleApproved, ToDo

admin.site.register(Schedule)
admin.site.register(ScheduleApproved)
admin.site.register(ToDo)
