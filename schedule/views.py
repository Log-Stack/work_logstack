import itertools
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max, Min
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader

from django.contrib.auth.models import User
from django.utils import timezone

from authy.models import Profile, TeamManager, Team
from .forms import NewScheduleWeekForm, NewScheduleDayForm, EventForm
from .models import Schedule, ScheduleApproved, ToDo, Event

COLORS = ['#0096c6', '#ff6939', '#fa3d00', '#6937a1', '#003458', '#008000']


@login_required
def index(request):
    user = request.user

    template = loader.get_template('schedule.html')

    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    schedule_exist = False
    is_staff = True
    schedule = Schedule.objects.filter(user=user, date=timezone.now().date(), work_type=1)
    if user.is_superuser:
        is_staff = False
    else:
        profile = Profile.objects.get(user=user)
        is_manager = TeamManager.objects.filter(team=profile.team, user=user).exists()
        if is_manager:
            is_staff = False
    if schedule.exists():
        schedule_exist = True

    context = {
        'user': user,
        'schedule_exist': schedule_exist,
        'is_staff': is_staff,
        'year': year,
        'month': month,
        'day': day,
    }

    return HttpResponse(template.render(context, request))


@login_required
def schedule_day(request, team_id, date):
    user = request.user.id
    selected_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")

    template = loader.get_template('schedule_day.html')

    context = {
        'user': user,
        'selected_date': selected_date,
        'selected_team': team_id,
    }

    return HttpResponse(template.render(context, request))


@login_required
def schedule_day_user_work_time(request):
    # team_id와 date를 받으면 팀원 리스트와 팀원의 해당 일자 예상 근무를 반환
    # events: [
    # {"resourceId":"team_id","title":"team_name",
    # "start":"2021-04-02T12:00:00+00:00","end":"2021-04-03T06:00:00+00:00",
    # "color" : COLORS[item.user.id % len(COLORS)]},
    # ...
    # ]
    team_id = request.GET.get('team_id')
    date = request.GET.get('selected_date')

    selected_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
    if team_id == '-1':  # 전체 검색
        users = Profile.objects.filter().values_list('user_id', flat=True)
    else:
        users = Profile.objects.filter(team=team_id).values_list('user_id', flat=True)

    if team_id == '-1':  # 전체 검색
        work_users = Schedule.objects.filter(user__in=users, date=selected_date, work_type=1).values_list('user_id')
        profiles = Profile.objects.filter(user__in=work_users)
    else:
        profiles = Profile.objects.filter(user__in=users)

    resources = []
    for item in profiles.values_list("user_id", "name"):
        resources.append(
            {'id': str(item[0]), 'title': item[1]}
        )

    work_times = Schedule.objects.filter(user__in=users, date=selected_date, work_type=1)
    events = []

    for item in work_times:
        url = "/schedule/todo/" + str(item.user.id) + "/" + item.date.strftime('%Y-%m-%d')
        events.append({
            'resourceId': str(item.user.id),
            'title': Profile.objects.get(user=item.user).name,
            'start': item.date.strftime('%Y-%m-%d') + "T" + item.start.isoformat(timespec='seconds') + "+00:00",
            'end': item.date.strftime('%Y-%m-%d') + "T" + item.end.isoformat(timespec='seconds') + "+00:00",
            'color': COLORS[item.user.id % len(COLORS)],
            'url': url,
            'description': ToDo.objects.get(schedule=item).contents,
        })

    vacation_times = Schedule.objects.filter(user__in=users, date=selected_date, work_type=2)
    for item in vacation_times.values_list("user_id", "date", "start", "end"):
        events.append({
            'resourceId': str(item[0]),
            'title': "휴가",
            'start': str(item[1]),
            'end': str(item[1]),
            'color': COLORS[item[0] % len(COLORS)],
        })
    result = {"resources": resources, 'event': events}

    return JsonResponse(result, safe=False)


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

            work_types.append(form.cleaned_data.get('work_type'))
            start_times.append(form.cleaned_data.get('start'))
            end_times.append(form.cleaned_data.get('end'))

            contents = form.cleaned_data.get('contents')

            for type_local, start_local, end_local in zip(work_types, start_times, end_times):
                if Schedule.objects.filter(user=user, date=week_start_date).exists():
                    schedule = Schedule.objects.get(user=user, date=week_start_date)
                    schedule.work_type = type_local
                    schedule.start = start_local
                    schedule.end = end_local
                    schedule.save()

                    todo = ToDo.objects.get(schedule=schedule)
                    todo.contents = contents
                    todo.save()
                else:
                    schedule, schedule_created = Schedule.objects.get_or_create(user=user, date=week_start_date,
                                                                                start=start_local,
                                                                                end=end_local, work_type=type_local)

                week_start_date += relativedelta(days=1)

    else:
        user = request.user

        selected_date = datetime(year, month, day).strftime("%Y-%m-%d")

        template = loader.get_template('schedule_register_day.html')
        form = NewScheduleDayForm()

        schedule, schedule_created = Schedule.objects.get_or_create(user=user, date=selected_date)

        form.fields['contents'].initial = ToDo.objects.get(schedule=schedule).contents



        context = {
            'user': user,
            'selected_date': selected_date,
            'forms': form,
        }

        return HttpResponse(template.render(context, request))


@login_required
def register_schedule_list_week(request, year, month, day):
    user = User.objects.get(id=request.user.id)
    user_profile = Profile.objects.get(user=user)

    week_start = datetime(year, month, day).strftime('%Y-%m-%d')
    week_end = (datetime(year, month, day) + relativedelta(days=6)).strftime('%Y-%m-%d')
    schedule = Schedule.objects.filter(user=user, date__range=[week_start, week_end]).order_by('date')

    schedule_list = list(schedule)
    schedule_data = []

    if len(schedule_list) == 0:
        for i in range(7):
            schedule_data.append(
                {'date': (datetime(year, month, day) + relativedelta(days=i)).strftime('%Y-%m-%d'),
                 'start': "00:00", 'end': "00:00",
                 'work_type': 0})

    for item in schedule_list:
        date = str(item.date)
        if item.start is not None and item.end is not None:
            start = str(item.start.strftime("%H:%M"))
            end = str(item.end.strftime("%H:%M"))
        else:
            start = "00:00"
            end = "00:00"
        work_type = item.work_type
        schedule_data.append(
            {'date': date, 'start': start, 'end': end, 'work_type': work_type})

    start_date = user_profile.start_date
    start_datetime = datetime(start_date.year, start_date.month, start_date.day)

    week_start = datetime(year, month, day)
    total_vacations_count = 0

    total_vacations_count += (week_start.year - start_datetime.year) * 12
    total_vacations_count += (week_start.month - start_datetime.month)
    if week_start.day - start_datetime.day < 0:
        total_vacations_count -= 1

    used_vacations_count = Schedule.objects.annotate(num_work_types=Count('work_type')).filter(user=user,
                                                                                               date__range=[start_date,
                                                                                                            week_start],
                                                                                               work_type=2).count()

    return JsonResponse({'date': schedule_data,
                         'vacation': "사용 휴가 / 총 휴가 | " + str(used_vacations_count) + " / " + str(
                             total_vacations_count)}, safe=False)


@login_required
def schedule_list_user(request, user_id, year, month):
    user = User.objects.get(id=user_id)

    day_start = datetime(year, month, 1).strftime('%Y-%m-%d')
    day_end = (datetime(year, month, 1) + relativedelta(months=2)).strftime('%Y-%m-%d')

    schedule = Schedule.objects.filter(user=user, date__range=[day_start, day_end]).order_by('user')

    user_profile = Profile.objects.get(user=user)
    schedule_list = list(schedule)
    result = []
    for item in schedule_list:
        name = str(user_profile.name)
        if item.start is not None and item.end is not None:
            start = str(item.start.strftime("%H:%M"))
            end = str(item.end.strftime("%H:%M"))
        else:
            start = "00:00"
            end = "00:00"
        work_type = item.work_type
        if work_type == 1:
            title = name + " | " + start + " : " + end
            color = user_profile.color
        elif work_type == 2:
            title = name + " | 휴가"
            color = COLORS[5]
        else:
            continue
        url = "/schedule/todo/" + str(item.user.id) + "/" + item.date.strftime('%Y-%m-%d')

        result.append({'title': title, 'start': item.date.strftime('%Y-%m-%d'),
                       'end': item.date.strftime('%Y-%m-%d'),
                       "color": color, 'url': url})

    return JsonResponse(result, safe=False)


@login_required
def schedule_list_edit(request):
    user = User.objects.get(id=request.user.id)
    year = int(request.GET.get('year', None))
    month = int(request.GET.get('month', None))

    day_start = datetime(year, month, 1).strftime('%Y-%m-%d')
    day_end = (datetime(year, month, 1) + relativedelta(months=2)).strftime('%Y-%m-%d')

    schedule = Schedule.objects.filter(user=user, date__range=[day_start, day_end]).order_by('date')

    user_profile = Profile.objects.get(user=user)

    schedule_list = list(schedule)

    events = []
    for item in schedule_list:
        name = str(user_profile.name)
        title = ""
        if item.work_type == 1:
            start = str(item.start.strftime("%H:%M"))
            end = str(item.end.strftime("%H:%M"))
            title = name + " | " + start + " : " + end
            color = COLORS[item.user.id % len(COLORS)]
        elif item.work_type == 2:
            title = name + " | " "휴가"
            color = COLORS[5]
        else:
            continue
        events.append({'title': title, 'start': item.date.strftime('%Y-%m-%d'),
                       'end': item.date.strftime('%Y-%m-%d'),
                       "color": color})
    return JsonResponse({"name": user_profile.name, "team": user_profile.team.name, "events": events}, safe=False)


@login_required
def schedule_list_team(request, team_id, year, month):
    result = []
    day_start = datetime(year, month, 1).strftime('%Y-%m-%d')
    day_end = (datetime(year, month, 1) + relativedelta(months=2)).strftime('%Y-%m-%d')

    if int(team_id) == -1:
        users = Profile.objects.filter().values_list('user_id', flat=True)
    else:
        users = Profile.objects.filter(team=team_id).values_list('user_id', flat=True)

    work_schedule = Schedule.objects.filter(user__in=users, date__range=[day_start, day_end], work_type=1) \
        .order_by('date')
    for item in list(work_schedule):
        name = Profile.objects.get(user=item.user.id).name
        start = str(item.start.strftime("%H:%M"))
        end = str(item.end.strftime("%H:%M"))
        url = "/schedule/todo/" + str(item.user.id) + "/" + item.date.strftime('%Y-%m-%d')
        result.append({'title': name + " | " + start + " ~ " + end, 'start': item.date.strftime('%Y-%m-%d'),
                       'end': item.date.strftime('%Y-%m-%d'),
                       "color": Profile.objects.get(user=item.user.id).color,
                       'url': url})

    vacation_schedule = Schedule.objects.filter(user__in=users, date__range=[day_start, day_end], work_type=2) \
        .values("date").distinct()

    for vacation_date in list(vacation_schedule):
        name_list = ""
        vacation_users = Schedule.objects.filter(user__in=users, date=vacation_date['date'], work_type=2)
        for item in vacation_users:
            name = Profile.objects.get(user=item.user.id).name
            if name is None:
                name_list += "익명, "
            else:
                name_list += Profile.objects.get(user=item.user.id).name + ", "

        result.append({'title': "휴가중 | " + name_list[:-2], 'start': item.date.strftime('%Y-%m-%d'),
                       'end': item.date.strftime('%Y-%m-%d'),
                       "color": COLORS[5]})
    return JsonResponse(result, safe=False)


@login_required
def schedule_summary_team(request):
    result = []
    team_id = int(request.GET.get('team', None))  # if team_id is -1 => summary by All Users
    year = int(request.GET.get('year', None))
    month = int(request.GET.get('month', None))

    day_start = datetime(year, month, 1).strftime('%Y-%m-%d')
    day_end = (datetime(year, month, 1) + relativedelta(months=2)).strftime('%Y-%m-%d')
    if team_id == -1:
        users = Profile.objects.filter().values_list('user_id', flat=True)
    else:
        users = Profile.objects.filter(team=team_id).values_list('user_id', flat=True)

    schedule = Schedule.objects.filter(user__in=users, date__range=[day_start, day_end], work_type__in=[1, 2]).order_by(
        'date')
    for work_date in schedule.values_list('date', flat=True).distinct():
        worker_count = Schedule.objects.annotate(num_work_types=Count('work_type')).filter(user__in=users,
                                                                                           date=work_date,
                                                                                           work_type=1).count()
        vacation_count = Schedule.objects.annotate(num_work_types=Count('work_type')).filter(user__in=users,
                                                                                             date=work_date,
                                                                                             work_type=2).count()
        times = Schedule.objects.filter(user__in=users, date=work_date).aggregate(start_time=Min('start'),
                                                                                  end_time=Max('end'))

        working_time = ""
        if times['start_time'] is not None and times['end_time'] is not None:
            start = times['start_time'].strftime("%H:%M")
            end = times['end_time'].strftime("%H:%M")
            working_time = start + " ~ " + end
        else:
            working_time = "근무 인원이 없습니다"

        result.append({'title': "근무 인원 : " + str(worker_count) + "명", 'start': work_date.strftime('%Y-%m-%d'),
                       'end': work_date.strftime('%Y-%m-%d'), "color": COLORS[0]})
        result.append(
            {'title': working_time, 'start': work_date.strftime('%Y-%m-%d'), 'end': work_date.strftime('%Y-%m-%d'),
             "color": COLORS[3]})
        result.append({'title': "휴가 인원 : " + str(vacation_count) + "명", 'start': work_date.strftime('%Y-%m-%d'),
                       'end': work_date.strftime('%Y-%m-%d'), 'color': COLORS[2]})

    if team_id == -1:
        birthday_users = Profile.objects.filter(birth_day__range=[day_start, day_end]).values()
        for day in list(birthday_users):
            result.append({'title': day['name'] + "님의 생일을 축하합니다!",
                           'start': day['birth_day'].strftime('%Y-%m-%d'),
                           'end': day['birth_day'].strftime('%Y-%m-%d'),
                           "color": COLORS[1]})

        events = Event.objects.filter(date__range=[day_start, day_end]).values()
        for event in events:
            result.append({'title': '일정 | ' + event['title'],
                           'start': event['date'].strftime('%Y-%m-%d'),
                           'end': event['date'].strftime('%Y-%m-%d'),
                           "color": '#fecb76', 'url': '/schedule/event/edit/' + str(event['id']) + '/', })

    return JsonResponse(result, safe=False)


@login_required
def schedule_todo(request, user_id, date):
    self_view = False
    if request.user.id is user_id:
        self_view = True

    if request.method == "GET":
        template = loader.get_template('schedule_todo.html')

        user = Profile.objects.get(user_id=user_id)
        schedule = Schedule.objects.get(user_id=user_id, date=date)
        todo, flag = ToDo.objects.get_or_create(schedule=schedule)
        start_time = schedule.start
        end_time = schedule.end

        context = {
            'self_view': self_view,
            'name': user.name,
            'id': user_id,
            'date': date,
            'context': todo.contents,
            'start_time': start_time,
            'end_time': end_time,
        }

        return HttpResponse(template.render(context, request))

    elif request.method == "POST":
        context = request.POST.get("context")
        schedule = Schedule.objects.get(user_id=request.user.id, date=date)
        todo, flag = ToDo.objects.get_or_create(schedule=schedule)
        todo.contents = context
        todo.save()

        return JsonResponse({"result": True}, safe=False)


@login_required
def register_schedule_today(request, year, month, day):
    user = User.objects.get(username=request.user)
    work_types = []
    start_times = []
    end_times = []

    form = NewScheduleDayForm(request.POST)
    if form.is_valid():
        week_start_date = form.cleaned_data.get('week_start_date')

        work_types.append(form.cleaned_data.get('work_type'))
        start_times.append(form.cleaned_data.get('start'))
        end_times.append(form.cleaned_data.get('end'))

        todo_contents = form.cleaned_data.get('contents')
        for type_local, start_local, end_local in zip(work_types, start_times, end_times):
            if Schedule.objects.filter(user=user, date=week_start_date).exists():
                schedule = Schedule.objects.get(user=user, date=week_start_date)
                schedule.work_type = type_local
                schedule.start = start_local
                schedule.end = end_local
                schedule.save()

                todo = ToDo.objects.get(schedule=schedule)
                todo.contents = todo_contents
                todo.save()
            else:
                schedule, schedule_created = Schedule.objects.get_or_create(user=user, date=week_start_date,
                                                                            start=start_local,
                                                                            end=end_local, work_type=type_local)
                todo = ToDo.objects.create(schedule=schedule, contents=todo_contents)

        return redirect('work_hour_check')
    else:
        user = request.user

        selected_date = datetime(year, month, day).strftime("%Y-%m-%d")

        template = loader.get_template('schedule_register_today.html')
        form = NewScheduleDayForm()

        schedule, schedule_created = Schedule.objects.get_or_create(user=user, date=selected_date)

        form.fields['contents'].initial = ToDo.objects.get(schedule=schedule).contents

        context = {
            'user': user,
            'selected_date': selected_date,
            'forms': form,
        }

        return HttpResponse(template.render(context, request))


@login_required
def schedule_event_add(request):
    if request.method == "GET":
        form = EventForm()
        context = {
            'form': form,
        }

        return render(request, 'schedule_event_add.html', context)

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            user_id = request.user.id
            title = form.cleaned_data.get('title')
            date = form.cleaned_data.get('date')
            start = form.cleaned_data.get('start')
            end = form.cleaned_data.get('end')
            content = form.cleaned_data.get('content')

            user = User.objects.get(pk=user_id)

            Event.objects.get_or_create(user=user, title=title, date=date, start=start, end=end, context=content)

        return render(request, 'schedule_event_add.html', {'form': EventForm()})


@login_required
def schedule_event_edit(request, event_id):
    self_view = False

    if request.method == "GET":
        template = loader.get_template('schedule_event_edit.html')

        event = Event.objects.get(pk=event_id)

        if request.user.id is event.user.id or request.user.is_superuser or TeamManager.objects.filter(
                user_id=request.user.id).exists():
            self_view = True

        context = {
            'event_id': event_id,
            'self_view': self_view,
            'title': event.title,
            'date': event.date.strftime("%Y-%m-%d"),
            'start': event.start.strftime("%H:%M"),
            'end': event.end.strftime("%H:%M"),
            'content': event.context,
        }

        return HttpResponse(template.render(context, request))

    elif request.method == "POST":
        event = Event.objects.get(pk=event_id)
        event.title = request.POST.get('title')
        event.start = request.POST.get('start')
        event.end = request.POST.get('end')
        event.date = request.POST.get('date')
        event.context = request.POST.get('content')
        event.save()

        return JsonResponse({"result": True}, safe=False)

    elif request.method == "DELETE":
        event = Event.objects.get(pk=event_id)
        event.delete()

        return JsonResponse({"result": True}, safe=False)
