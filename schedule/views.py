from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template import loader

from django.contrib.auth.models import User
from authy.models import Profile, TeamManager
from .forms import NewScheduleForm
from .models import Schedule, ScheduleApproved


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
    selected_date = datetime.today().strftime("%Y-%m-%d")
    if TeamManager.objects.filter(user=user).exists():
        template = loader.get_template('schedule_approved.html')
        team = TeamManager.objects.get(user=user)
        context = {
            'user': user,
            'team': team.team,
            'team_id': team.team.id,
            'selected_date': selected_date,
        }

        return HttpResponse(template.render(context, request))


@login_required
def register_index(request):
    user = User.objects.get(username=request.user)
    work_types = []
    start_times = []
    end_times = []
    if request.method == 'POST':
        form = NewScheduleForm(request.POST)
        if form.is_valid():
            week_start_date = form.cleaned_data.get('week_start_date')
            approved, is_approved = ScheduleApproved.objects.get_or_create(user=user, week_start_date=week_start_date)

            work_types.append(form.cleaned_data.get('sun_work_type'))
            start_times.append(form.cleaned_data.get('sun_start'))
            end_times.append(form.cleaned_data.get('sun_end'))

            work_types.append(form.cleaned_data.get('mon_work_type'))
            start_times.append(form.cleaned_data.get('mon_start'))
            end_times.append(form.cleaned_data.get('mon_end'))

            work_types.append(form.cleaned_data.get('tue_work_type'))
            start_times.append(form.cleaned_data.get('tue_start'))
            end_times.append(form.cleaned_data.get('tue_end'))

            work_types.append(form.cleaned_data.get('wed_work_type'))
            start_times.append(form.cleaned_data.get('wed_start'))
            end_times.append(form.cleaned_data.get('wed_end'))

            work_types.append(form.cleaned_data.get('thu_work_type'))
            start_times.append(form.cleaned_data.get('thu_start'))
            end_times.append(form.cleaned_data.get('thu_end'))

            work_types.append(form.cleaned_data.get('fri_work_type'))
            start_times.append(form.cleaned_data.get('fri_start'))
            end_times.append(form.cleaned_data.get('fri_end'))

            work_types.append(form.cleaned_data.get('sat_work_type'))
            start_times.append(form.cleaned_data.get('sat_start'))
            end_times.append(form.cleaned_data.get('sat_end'))

            if is_approved:  # do create
                for type_local, start_local, end_local in zip(work_types, start_times, end_times):
                    schedule = Schedule.objects.create(user=user, date=week_start_date, start=start_local,
                                                       end=end_local, work_type=type_local)
                    week_start_date += timedelta(days=1)
            else:  # do update
                approved.approved_type = ScheduleApproved.APPROVED_TYPES[0][0]
                approved.save()
                for type_local, start_local, end_local in zip(work_types, start_times, end_times):
                    schedule = Schedule.objects.get(user=user, date=week_start_date)
                    schedule.work_type = type_local
                    schedule.start = start_local
                    schedule.end = end_local
                    schedule.save()
                    week_start_date += timedelta(days=1)

            return redirect('schedule-index')
    else:
        user = request.user

        selected_date = datetime.today().strftime("%Y-%m-%d")

        template = loader.get_template('schedule_register.html')
        form = NewScheduleForm()
        context = {
            'user': user,
            'selected_date': selected_date,
            'forms': form
        }

        return HttpResponse(template.render(context, request))

    user = request.user
    template = loader.get_template('schedule_register.html')
    form = NewScheduleForm()
    context = {
        'user': user,
        'forms': form
    }

    return HttpResponse(template.render(context, request))


@login_required
def schedule_list_user(request, user_id, year, month):
    user = User.objects.get(id=user_id)
    schedule = Schedule.objects.filter(user=user, date__year=year, date__month=month).order_by('user')
    schedule = schedule | Schedule.objects.filter(user=user, date__year=year, date__month=str(int(month) + 1)).order_by(
        'user')
    user_profile = Profile.objects.get(user=user)
    schedule_list = list(schedule)
    result = []
    for item in schedule_list:
        name = str(user_profile.name)
        date = str(item.date)
        if item.start is not None and item.end is not None:
            start = str(item.start.strftime("%H:%M"))
            end = str(item.end.strftime("%H:%M"))
        else:
            start = "00:00"
            end = "00:00"
        work_type = item.work_type
        result.append(
            {'name': name, 'date': date, 'start': start, 'end': end, 'work_type': work_type, 'color': user.id % 5})

    return JsonResponse(result, safe=False)


@login_required
def schedule_list_team(request, team_id, year, month):
    result = []

    users = Profile.objects.filter(team=team_id)
    for user in users:
        print(user.name)
        schedule = Schedule.objects.filter(user=user.user_id, date__year=year, date__month=month).order_by('user_id')
        schedule = schedule | Schedule.objects.filter(user=user.user_id, date__year=year,
                                                      date__month=str(int(month) + 1)).order_by('user_id')
        for item in list(schedule):
            name = str(user.name)
            date = str(item.date)
            if item.start is not None and item.end is not None:
                start = str(item.start.strftime("%H:%M"))
                end = str(item.end.strftime("%H:%M"))
            else:
                start = "00:00"
                end = "00:00"
            work_type = item.work_type
            result.append(
                {'name': name, 'date': date, 'start': start, 'end': end, 'work_type': work_type, 'color': user.id % 5})
    return JsonResponse(result, safe=False)
