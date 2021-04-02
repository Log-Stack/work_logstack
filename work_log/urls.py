from django.urls import path
from .views import (
    start_working,
    end_working,
    work_log_list,
    work_log_write,
    work_log_detail,
    work_log_edit,
    work_hour_edit,
    work_hour_check,
    work_log_written,
    work_logs_by_team,
    work_logs_by_user,
    work_logs_summary_team,
)

urlpatterns = [
    path('start/', start_working, name='start_working'),
    path('end/', end_working, name='end_working'),
    path('list/', work_log_list, name='work_log_list'),
    path('write/', work_log_write, name='work_log_write'),
    path('written/', work_log_written, name='work_log_written'),
    path('edit/<int:pk>/', work_log_edit, name='work_log_edit'),
    path('detail/<int:pk>/', work_log_detail, name='work_log_detail'),
    path('work_hour_check/', work_hour_check, name='work_hour_check'),
    path('work_hour_edit/<int:pk>/', work_hour_edit, name='work_hour_edit'),
    path('work_logs/user/<user_id>/<year>/<month>', work_logs_by_user, name='work_logs_by_user'),
    path('work_logs/team/<team_id>/<year>/<month>', work_logs_by_team, name='work_logs_by_team'),
    path('work_logs/summary/', work_logs_summary_team, name='work_logs_summary_team'),
]