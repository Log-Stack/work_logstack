from django.urls import path
from .views import start_working, end_working, work_log_list, work_log_write, work_log_detail, work_log_edit

urlpatterns = [
    path('start/', start_working, name='start_working'),
    path('end/', end_working, name='end_working'),
    path('list/', work_log_list, name='work_log_list'),
    path('write/', work_log_write, name='work_log_write'),
    path('edit/<int:pk>/', work_log_edit, name='work_log_edit'),
    path('detail/<int:pk>/', work_log_detail, name='work_log_detail'),
]