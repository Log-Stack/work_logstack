from django.urls import path
from .views import *

urlpatterns = [
    path('start/', start_working, name='start_working'),
    path('end/', end_working, name='end_working'),
    path('list/', work_log_list, name='work_log_list'),
    path('write/', work_log_write, name='work_log_write'),
    path('previous_write/<int:work_hour_pk>/', previous_work_log_write, name='previous_work_log_write'),
    path('written/', work_log_written, name='work_log_written'),
    path('edit/<int:pk>/', work_log_edit, name='work_log_edit'),
    path('edit_page/<int:pk>/', work_log_edit_page, name='work_log_edit_page'),
    path('detail/<int:pk>/', work_log_detail, name='work_log_detail'),
    path('detail_page/<int:pk>/', work_log_detail_page, name='work_log_detail_page'),
    path('work_hour_check/', work_hour_check, name='work_hour_check'),
    path('work_hour_edit/<int:pk>/', work_hour_edit, name='work_hour_edit'),
    path('work_logs/user/<user_id>/<year>/<month>', work_logs_by_user, name='work_logs_by_user'),
    path('work_logs/team/<team_id>/<year>/<month>', work_logs_by_team, name='work_logs_by_team'),
    path('work_logs/summary/', work_logs_summary_team, name='work_logs_summary_team'),
]