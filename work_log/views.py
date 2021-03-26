from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from django.utils import timezone
import datetime

from django.contrib.auth.models import User

from .models import WorkHour, WorkLog
from .forms import WorkLogForm, WorkHourForm
from authy.models import Team, TeamManager, Profile, Position
from django.core.paginator import Paginator


@login_required
def start_working(request):
    user = request.user
    already_work_hour = WorkHour.objects.filter(user=user).filter(date=timezone.now().date()).exists()
    if not already_work_hour:
        work_hour = WorkHour(user=user)
        work_hour.save()
    return redirect('work_hour_check')


@login_required
def end_working(request):
    user = request.user
    work_hour = WorkHour.objects.filter(user=user).filter(date=timezone.now().date()).first()
    if work_hour:
        work_hour.end_time = timezone.now()
        work_hour.save()
    return redirect('work_hour_check')


@login_required
def work_hour_check(request):
    user = request.user
    work_hour = WorkHour.objects.filter(user=user).filter(date=timezone.now().date()).first()
    context = {
        'work_hour': work_hour
    }
    return render(request, 'work_hour_check.html', context)


@login_required
def work_hour_edit(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    team_manager = TeamManager.objects.filter(team=profile.team).filter(user=user).exists()
    if team_manager:
        work_hour = get_object_or_404(WorkHour, pk=pk)
        member = Profile.objects.get(user=work_hour.user)
        if request.method == "POST":
            form = WorkHourForm(request.POST, instance=work_hour)
            if form.is_valid():
                form.save()
                return redirect('work_hour_edit', pk)
        else:
            form = WorkHourForm(instance=work_hour)

        context = {
            'form': form,
            'work_hour': work_hour,
            'member': member,
        }
        return render(request, 'work_hour_edit.html', context)
    return redirect('index')


@login_required
def work_log_write(request):
    if request.method == "POST":
        form = WorkLogForm(request.POST)
        if form.is_valid():
            work_log = form.save(commit=False)
            work_log.user = request.user
            work_log.save()
            return redirect('work_log_detail', pk=work_log.pk)
    else:
        work_log = WorkLog.objects.filter(user=request.user).filter(create_time__date=timezone.now().date()).first()
        if work_log:
            return redirect('work_log_detail', pk=work_log.pk)
        form = WorkLogForm()
    return render(request, 'work_log_write.html', {'form': form})


@login_required()
def work_log_edit(request, pk):
    work_log = get_object_or_404(WorkLog, pk=pk)
    if work_log.user == request.user:
        if request.method == "POST":
            form = WorkLogForm(request.POST, instance=work_log)
            if form.is_valid():
                work_log = form.save(commit=False)
                work_log.user = request.user
                work_log.is_updated = True
                work_log.save()
                return redirect('work_log_detail', pk=work_log.pk)
        else:
            form = WorkLogForm(instance=work_log)
        return render(request, 'work_log_write.html', {'form': form})
    else:
        return redirect('work_log_list')


@login_required
def work_log_detail(request, pk):
    work_log = get_object_or_404(WorkLog, pk=pk)
    user = work_log.user
    date = work_log.create_time.date()
    work_hour = WorkHour.objects.filter(user=user).filter(date=date).first()
    context = {
        'work_log': work_log,
        'work_hour': work_hour
    }
    return render(request, 'work_log_detail.html', context)


@login_required
def work_log_list(request):
    work_logs = WorkLog.objects.all()
    search = ""
    start_date = ""
    end_date = ""
    team = "all"
    member = "직원 선택"

    if request.method == "POST":
        search = request.POST.get('search')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        team_id = request.POST.get('team')
        member_id = request.POST.get('member')

        # selector 처리
        profiles = Profile.objects.all()
        if team_id != 'all':
            profiles = profiles.filter(team=team_id)
            team = team_id
        if member_id != '직원 선택':
            profiles = profiles.filter(user=member_id)
            member = member_id

        # 검색어 처리
        user_ids = []
        profiles = profiles.filter(name__icontains=search)
        for profile in profiles:
            user_ids.append(profile.user.pk)
        work_logs = WorkLog.objects.filter(user_id__in=user_ids)

        # 날짜 처리
        if start_date:
            work_logs = work_logs.filter(create_time__date__gte=start_date)
        if end_date:
            work_logs = work_logs.filter(create_time__date__lte=end_date)

    work_logs = work_logs.order_by('-create_time')

    # Pagination
    paginator = Paginator(work_logs, 12)
    page_number = request.GET.get('page')
    work_logs_paginator = paginator.get_page(page_number)

    context = {
        'team': team,
        'member': member,
        'work_logs': work_logs_paginator,
        'start_date': start_date,
        'end_date': end_date,
        'search': search,
    }
    return render(request, 'work_log_list.html', context)



