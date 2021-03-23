from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import loader

from django.contrib.auth.models import User
from authy.models import Profile
from .forms import NewScheduleForm
from .models import Schedule


@login_required
def index(request):
    user = request.user

    template = loader.get_template('schedule.html')

    context = {
        'user': user,
    }

    return HttpResponse(template.render(context, request))


@login_required
def approved(request):
    user = request.user

    template = loader.get_template('schedule_approved.html')

    context = {
        'user': user,
    }

    return HttpResponse(template.render(context, request))


@login_required
def register_index(request):
    user = request.user
    template = loader.get_template('schedule_register.html')
    form = NewScheduleForm()
    context = {
        'user': user,
        'forms': form
    }

    return HttpResponse(template.render(context, request))

@login_required
def register_select_date(request, year, month, date):
    user = request.user
    selected_date = year + "-" + month + "-" + date
    template = loader.get_template('schedule_register.html')
    form = NewScheduleForm()
    context = {
        'user': user,
        'selected_date': selected_date,
        'forms': form
    }

    return HttpResponse(template.render(context, request))


@login_required
def schedule_list_user(request, user_id, year, month):
    user = User.objects.get(id=user_id)
    schedule = Schedule.objects.filter(user=user, date__year=year, date__month=month).order_by('user')
    user_profile = Profile.objects.get(user=user_id)
    schedule_list = list(schedule)
    result = []
    for item in schedule_list:
        name = str(user_profile.name)
        date = str(item.date)
        start = str(item.start.strftime("%H:%M"))
        end = str(item.end.strftime("%H:%M"))
        work_type = item.work_type
        result.append(
            {'name': name, 'date': date, 'start': start, 'end': end, 'work_type': work_type, 'color': user.id % 5})

    return JsonResponse(result, safe=False)


@login_required
def schedule_list_team(request, team_id, year, month):
    result = []

    users = Profile.objects.filter(team=team_id)
    for user in users:
        schedule = Schedule.objects.filter(user=user.user_id, date__year=year, date__month=month).order_by('user_id')
        for item in list(schedule):
            name = str(user.name)
            date = str(item.date)
            start = str(item.start.strftime("%H:%M"))
            end = str(item.end.strftime("%H:%M"))
            work_type = item.work_type
            result.append(
                {'name': name, 'date': date, 'start': start, 'end': end, 'work_type': work_type, 'color': user.id % 5})

    return JsonResponse(result, safe=False)
