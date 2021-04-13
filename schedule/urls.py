from django.urls import path

from schedule.views import index, schedule_day, approved, register_index, schedule_list_user, schedule_list_team, \
    approved_list, \
    approved_user, register_schedule_list_week, register_schedule_day, schedule_summary_team, schedule_list_edit, \
    schedule_day_user_work_time, schedule_todo, register_schedule_today, \
    schedule_event_add, schedule_event_edit

urlpatterns = [
    path('', index, name='schedule-index'),
    path('day/api/', schedule_day_user_work_time, name='schedule-day-user-work-time'),
    path('day/<team_id>/<date>/', schedule_day, name='schedule-day'),

    path('approved/', approved, name='schedule-approved'),
    path('approved/list/<team_id>/<year>/<month>/<day>', approved_list, name='schedule-approved-list'),
    path('approved/<user>/<year>/<month>/<day>/<type>', approved_user, name='schedule-approved-list'),

    path('register/', register_index, name='schedule-register'),
    path('register/day/<int:year>/<int:month>/<int:day>', register_schedule_day, name='schedule-register-day'),
    path('register/list/week/<int:year>/<int:month>/<int:day>', register_schedule_list_week,
         name='schedule-register-list-user-day'),

    path('list/user/<user_id>/<int:year>/<int:month>', schedule_list_user, name='schedule-list-user'),
    path('list/edit/', schedule_list_edit, name='schedule-list-user'),
    path('list/team/<team_id>/<int:year>/<int:month>', schedule_list_team, name='schedule-list-team'),
    path('list/summary/', schedule_summary_team, name='schedule-summary-team'),

    path('todo/<int:user_id>/<date>', schedule_todo, name='schedule-summary-team'),

    path('event/add', schedule_event_add, name='schedule-event'),
    path('event/edit/<event_id>/', schedule_event_edit, name='schedule-event'),

    path('today/register/<int:year>/<int:month>/<int:day>', register_schedule_today, name='schedule-register-today'),
]
