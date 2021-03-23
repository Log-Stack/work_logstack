from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from django.utils import timezone

from django.contrib.auth.models import User

from .models import WorkHour, WorkLog
from .forms import WorkLogForm
from authy.models import Team, TeamManager, Profile, Position


@login_required
def start_working(request):
    user = request.user
    work_hour = WorkHour(user=user)
    work_hour.save()
    return redirect('index')


@login_required
def end_working(request):
    user = request.user
    work_hour = WorkHour.objects.filter(user=user).filter(date=timezone.now().date()).first()
    work_hour.end_time = timezone.now()
    work_hour.save()
    return redirect('work_log_write')


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
    teams = Team.objects.all()
    work_logs = WorkLog.objects.order_by('-create_time')
    start_date = ""
    end_date = ""

    if request.method == "POST":
        search = request.POST.get('search')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        result_start_date = start_date
        result_end_date = end_date

        if result_start_date == "":
            result_start_date = "2021-03-01"
        if result_end_date == "":
            result_end_date = "2999-01-01"

        user_ids = []
        profiles = Profile.objects.filter(name__icontains=search)

        for profile in profiles:
            user_ids.append(profile.user.pk)

        work_logs = WorkLog.objects.filter(user_id__in=user_ids).filter(create_time__gte=result_start_date).filter(create_time__lte=result_end_date).order_by('-create_time')

        context = {
            'teams': teams,
            'work_logs': work_logs,
            'start_date': start_date,
            'end_date': end_date,
        }
    else:
        context = {
            'teams': teams,
            'work_logs': work_logs,
            'start_date': start_date,
            'end_date': end_date,
        }
    return render(request, 'work_log_list.html', context)



