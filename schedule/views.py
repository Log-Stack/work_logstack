import itertools
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max, Min
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template import loader

from django.contrib.auth.models import User
from authy.models import Profile, TeamManager, Team
from .forms import NewScheduleWeekForm, NewScheduleDayForm
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
def approved_list(request, team_id, year, month, day):
    result = []

    team = Team.objects.get(id=team_id)

    profiles = Profile.objects.filter(team=team)
    approved_type = ""
    for profile in list(profiles):
        exist = False
        result_user = []
        user = profile.user
        approved = ScheduleApproved.objects.filter(user=user, week_start_date__year=year, week_start_date__month=month,
                                                   week_start_date__day=day)
        if approved.exists():
            approved_type = ScheduleApproved.objects.get(user=user, week_start_date__year=year,
                                                         week_start_date__month=month,
                                                         week_start_date__day=day).approved_type
            exist = True
            for index in range(7):
                schedule = Schedule.objects.get(user=user, date__year=year, date__month=month, date__day=day)
                start = schedule.start
                end = schedule.end
                if start is not None and end is not None:
                    start = str(start.strftime("%H:%M"))
                    end = str(end.strftime("%H:%M"))
                else:
                    start = "00:00"
                    end = "00:00"
                work_type = schedule.work_type
                result_user.append(
                    {'start': start, 'end': end, 'work_type': work_type})
        else:
            approved_type = -1
        result.append({'name': str(user.username), 'exist': exist, 'approved': approved_type,
                       "date": result_user})
    return JsonResponse(result, safe=False)


@login_required
def approved_user(request, user, year, month, day, type):
    user = User.objects.get(username=user)
    approved = ScheduleApproved.objects.filter(user=user, week_start_date__year=year, week_start_date__month=month,
                                               week_start_date__day=day)
    if approved.exists():
        approved = ScheduleApproved.objects.get(user=user, week_start_date__year=year,
                                                week_start_date__month=month,
                                                week_start_date__day=day)
        approved.approved_type = type
        approved.save()

    return JsonResponse("complete", safe=False)


@login_required
def register_index(request):
    user = User.objects.get(username=request.user)
    work_types = []
    start_times = []
    end_times = []
    if request.method == 'POST':
        form = NewScheduleWeekForm(request.POST)
        if form.is_valid():
            week_start_date = form.cleaned_data.get('week_start_date')
            approved, is_approved = ScheduleApproved.objects.get_or_create(user=user,
                                                                           week_start_date=week_start_date)

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
                    week_start_date += relativedelta(days=1)
            else:  # do update
                approved.approved_type = ScheduleApproved.APPROVED_TYPES[0][0]
                approved.save()
                for type_local, start_local, end_local in zip(work_types, start_times, end_times):
                    schedule = Schedule.objects.get(user=user, date=week_start_date)
                    schedule.work_type = type_local
                    schedule.start = start_local
                    schedule.end = end_local
                    schedule.save()
                    week_start_date += relativedelta(days=1)

            return redirect('schedule-index')
    else:
        user = request.user

        selected_date = datetime.today().strftime("%Y-%m-%d")

        template = loader.get_template('schedule_register.html')
        form = NewScheduleWeekForm()
        context = {
            'user': user,
            'selected_date': selected_date,
            'forms': form
        }

        return HttpResponse(template.render(context, request))


@login_required
def register_schedule_day(request, year, month, day):
    user = User.objects.get(username=request.user)
    work_types = []
    start_times = []
    end_times = []
    if request.method == 'POST':
        form = NewScheduleDayForm(request.POST)
        if form.is_valid():
            week_start_date = form.cleaned_data.get('week_start_date')
            approved, is_approved = ScheduleApproved.objects.get_or_create(user=user,
                                                                           week_start_date=week_start_date)

            work_types.append(form.cleaned_data.get('work_type'))
            start_times.append(form.cleaned_data.get('start'))
            end_times.append(form.cleaned_data.get('end'))

            if is_approved:  # do create
                for type_local, start_local, end_local in zip(work_types, start_times, end_times):
                    schedule = Schedule.objects.create(user=user, date=week_start_date, start=start_local,
                                                       end=end_local, work_type=type_local)
                    week_start_date += relativedelta(days=1)
            else:  # do update
                approved.approved_type = ScheduleApproved.APPROVED_TYPES[0][0]
                approved.save()
                for type_local, start_local, end_local in zip(work_types, start_times, end_times):
                    schedule = Schedule.objects.get(user=user, date=week_start_date)
                    schedule.work_type = type_local
                    schedule.start = start_local
                    schedule.end = end_local
                    schedule.save()
                    week_start_date += relativedelta(days=1)

            return redirect('schedule-index')
    else:
        user = request.user

        selected_date = datetime(year, month, day).strftime("%Y-%m-%d")

        template = loader.get_template('schedule_register_day.html')
        form = NewScheduleDayForm()
        context = {
            'user': user,
            'selected_date': selected_date,
            'forms': form
        }

        return HttpResponse(template.render(context, request))


@login_required
def register_schedule_list_week(request, year, month, day):
    user = User.objects.get(id=request.user.id)

    week_start = datetime(year, month, day).strftime('%Y-%m-%d')
    week_end = (datetime(year, month, day) + relativedelta(days=6)).strftime('%Y-%m-%d')
    schedule = Schedule.objects.filter(user=user, date__range=[week_start, week_end]).order_by('date')

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
            {'date': date, 'start': start, 'end': end, 'work_type': work_type})

    return JsonResponse(result, safe=False)


@login_required
def schedule_list_user(request, user_id, year, month):
    user = User.objects.get(id=user_id)
    schedule = Schedule.objects.filter(user=user, date__year=year, date__month=month).order_by('user')
    schedule = schedule | Schedule.objects.filter(user=user, date__year=year,
                                                  date__month=str(int(month) + 1)).order_by(
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
        schedule = Schedule.objects.filter(user=user.user_id, date__year=year, date__month=month).order_by(
            'user_id')
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
                {'name': name, 'date': date, 'start': start, 'end': end, 'work_type': work_type,
                 'color': user.id % 5})
    return JsonResponse(result, safe=False)


@login_required
def schedule_summary_team(request):
    result = []
    team_id = request.GET.get('team', None)
    year = int(request.GET.get('year', None))
    month = int(request.GET.get('month', None))

    day_start = datetime(year, month, 1).strftime('%Y-%m-%d')
    day_end = (datetime(year, month, 1) + relativedelta(months=1)).strftime('%Y-%m-%d')

    users = Profile.objects.filter(team=team_id).values_list('id', flat=True)
    schedule = Schedule.objects.filter(user__in=users, date__range=[day_start, day_end]).order_by('date')

    for work_date in schedule.values_list('date', flat=True).distinct():
        # test = Schedule.objects.filter(user__in=users, date=work_date).annotate(Count('work_type'))
        worker_count = Schedule.objects.annotate(num_work_types=Count('work_type')).filter(user__in=users,
                                                                                           date=work_date,
                                                                                           work_type=1).count()
        vacation_count = Schedule.objects.annotate(num_work_types=Count('work_type')).filter(user__in=users,
                                                                                             date=work_date,
                                                                                             work_type=2).count()
        times = Schedule.objects.filter(user__in=users, date=work_date).aggregate(start_time=Min('start'),
                                                                                  end_time=Max('end'))
        start = ""
        end = ""
        if times['start_time'] is not None and times['end_time'] is not None:
            start = times['start_time'].strftime("%H:%M")
            end = times['end_time'].strftime("%H:%M")
        result.append({
            'date': work_date.strftime('%Y-%m-%d'),
            'start': start,
            'end': end,
            'worker_count': worker_count,
            'vacation_count': vacation_count,
        })
    return JsonResponse(result, safe=False)
