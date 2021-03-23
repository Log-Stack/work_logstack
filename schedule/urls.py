from django.urls import path

from schedule.views import index, approved, register_index, schedule_list_user, schedule_list_team, register_select_date

urlpatterns = [
    path('', index, name='schedule-index'),
    path('approved/', approved, name='schedule-approved'),
    path('register/', register_index, name='schedule-register'),
    path('register/<year>/<month>/<date>', register_select_date, name='schedule-register-select-date'),
    path('list/user/<user_id>/<year>/<month>', schedule_list_user, name='schedule-list-user'),
    path('list/team/<team_id>/<year>/<month>', schedule_list_team, name='schedule-list-team'),
]
