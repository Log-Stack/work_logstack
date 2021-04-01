from django.urls import path

from schedule.views import index, approved, register_index, schedule_list_user, schedule_list_team, approved_list, \
    approved_user, register_schedule_list_week, register_schedule_day, schedule_summary_team

urlpatterns = [
    path('', index, name='schedule-index'),

    path('approved/', approved, name='schedule-approved'),
    path('approved/list/<team_id>/<year>/<month>/<day>', approved_list, name='schedule-approved-list'),
    path('approved/<user>/<year>/<month>/<day>/<type>', approved_user, name='schedule-approved-list'),

    path('register/', register_index, name='schedule-register'),
    path('register/day/<int:year>/<int:month>/<int:day>', register_schedule_day, name='schedule-register-day'),
    path('register/list/week/<int:year>/<int:month>/<int:day>', register_schedule_list_week,
         name='schedule-register-list-user-day'),

    path('list/user/<user_id>/<year>/<month>', schedule_list_user, name='schedule-list-user'),
    path('list/team/<int:team_id>/<int:year>/<int:month>', schedule_list_team, name='schedule-list-team'),
    path('list/summary/', schedule_summary_team, name='schedule-summary-team'),
]
