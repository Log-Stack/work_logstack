from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template import loader
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authy.forms import TeamCreateForm, UserCreateForm, ProfileForm, SignupForm, ChangePasswordForm, \
    CustomAuthenticationForm, MemberInfoForm
from authy.models import Team, Profile
from authy.serializers import TeamSerializer, ProfileSerializer
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

from authy.models import TeamManager, Position
from work_log.models import WorkHour, WorkLog
from django.utils import timezone
import datetime



def login(request):
    if request.user.is_authenticated:
        return redirect('schedule-index')
    if request.method == "POST":
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            is_manager = TeamManager.objects.filter(user=form.get_user()).exists()
            user = form.get_user()
            profile = Profile.objects.filter(user=user)

            if profile[0].name == None:
                return redirect('editprofile')

            if is_manager or user.is_superuser:
                return redirect('schedule-index')
            else:
                return redirect('work_hour_check')
    else:
        form = CustomAuthenticationForm()
    context = {"form": form}
    return render(request, "login.html", context)


@login_required
def index(request):
    user = request.user

    template = loader.get_template('index.html')

    context = {
        'user': user,
    }

    return HttpResponse(template.render(context, request))


# @login_required
# def CreateUserView(request):
#     if request.method == 'POST':
#
#         signup_form = SignupForm(request.POST)
#         team_form = TeamForm(request.POST)
#
#         if signup_form.is_valid() and team_form.is_valid():
#
#             signup_form.save()
#             team_form.save()
#             return redirect('index')
#
#         else:
#             context = {
#                 'signup_form': signup_form,
#                 'team_form': team_form,
#             }
#
#     else:
#         context = {
#             'signup_form': SignupForm(),
#             'team_form': TeamForm(),
#         }
#
#     return render(request, 'user_create.html', context)

@login_required
def CreateUserView(request):
    teams = list(Team.objects.all().values_list('name', flat=True))
    positions = list(Position.objects.all().values_list('name', flat=True))

    if request.method == 'POST':
        form = SignupForm(request.POST)
        #form.fields['password'].widget.render_value = True

        if form.is_valid():

            username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password')
            password = 'logstack'
            user = User.objects.create_user(username=username, password=password)


            team_name = request.POST.get('team')
            position_name = request.POST.get('position')
            team = Team.objects.get(name=team_name)
            position = Position.objects.get(name=position_name)
            profile = Profile(user=user, team=team, position=position)
            profile.save()
            return redirect('schedule-index')
    else:
        form = SignupForm()

    context = {
        'form': form,
        'teams': teams,
        'positions' : positions,
    }

    return render(request, 'user_create.html', context)


# Leader of team creates team
@login_required
def CreateTeamView(request):
    teams = list(Team.objects.all().values_list('name', flat=True))
    if request.method == 'POST':
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.name = form.cleaned_data.get('name')
            obj.save()
            print("ok")
            return redirect('index')
        else:
            print("not ok")
    else:
        form = TeamCreateForm()

    context = {
        'form': form,
        'teams': teams,
    }

    return render(request, 'team_create.html', context)




@login_required
def ProfileView(request):
    user_id = request.user.id
    profile = get_object_or_404(Profile, user_id=user_id)
    context = {
        'profile': profile
    }

    return render(request,'user_info.html', context)


@login_required
def EditProfileData(request, pk):
    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        form = MemberInfoForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('manage_detail', pk)
    return redirect('index')


# Staff edits profile
#   fields = ['name', 'birth_day', 'phone_number', 'email_address']
def EditProfileView(request):
    user = request.user
    profile = Profile.objects.filter(user=user)[0]
    #print(profile.birth_day)2021-03-12

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user

            user = User.objects.get(username=request.user)
            user.email = form.cleaned_data.get('email_address')
            user.save()
            obj.save()
            return redirect('index')
        else:
            print("not ok")
            print(form.errors)
    else:
        form = ProfileForm()
        print("not POST")

    context = {
        'id': request.user.username,
        'form': form,
        'profile': profile,
    }
    return render(request, 'user_info_edit.html', context)



#User Change Password
def ChangePWView(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('changepwdone')
    else:
        form = ChangePasswordForm(instance=user)

    context = {
        'form': form,
    }

    return render(request, 'user_password.html', context)


def ChangePWDoneView(request):
    return render(request, 'change_password_done.html')



@login_required
def UserSearchView(request):
    #직원 이름으로 검
    query = request.GET.get('q')
    context = {}

    if query:
        users = Profile.objects.filter(Q(name__icontains=query))
        # profiles = list(users)
        # print(list(users)[0].user_id)

        #Pagination
        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        context = {
            'users': users_paginator,
            # 'profiles':profiles,
        }
    template = loader.get_template('user_search.html')


    return HttpResponse(template.render(context, request))



@login_required
def SearchAllView(request):
    teams = Team.objects.all().order_by('name')
    profile = Profile.objects.all().order_by('name')
    teams_exists = []

    for team in teams:
        if len(profile.filter(team=team.pk))!=0:
            teams_exists.append(team)

    context = {
        'users': profile,
        'teams' : teams_exists,
    }
    return render(request,'user_search_all.html', context)


@login_required
def SearchSelectView(request):
    teams = list(Team.objects.all().values_list('name', flat=True))
    context={
        'teams':teams,
    }
    return render(request,'user_search_result.html',context)


@login_required
def UserDetailView(request, pk):
    profile = get_object_or_404(Profile, user_id=pk)

    if request.method == "POST":
        work_start_date = request.POST.get('work_start_date')
        work_end_date = request.POST.get('work_end_date')

    context = {
        'profile': profile,
        # 'work_start_date': work_start_date,
        # 'work_end_date': work_end_date,
    }

    return render(request,'user_search_result.html', context)


# api view
class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
def TeamMates(request, team):
    if request.method == 'GET':
        queryset = Profile.objects.filter(team=team)
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


# 팀원 관리

def check_manager(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get_or_create(user=request.user)[0]
        return {
            'team_manager': TeamManager.objects.filter(user=request.user).exists() or request.user.is_superuser,
            'name': profile.name
        }
    else:
        return {
            'team_manager': False
        }
        #user = request.user

        #team_manager = TeamManager.objects.filter(user=user).exists()
        #print(type(team_manager))
    # return {'team_manager': team_manager}
# @login_required
# def super_manage_list(request, pk):
#     user = request.user
#
#
#     return render(request, 'index.html')


@login_required
def manage_list(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    team_manager = TeamManager.objects.filter(team=profile.team).filter(user=user).first()

    if user.is_superuser:
        team_name = 'all'
        teams = Team.objects.all()
        team_members = Profile.objects.all()

        if request.method == "POST":
            search = request.POST.get('search')
            team_name = request.POST.get('team_name')

            if team_name != 'all':
                team = Team.objects.get(name=team_name)
                team_members = team_members.filter(team=team)

            result = team_members
            result = result.filter(name__icontains=search)

            context = {
                'teams': teams,
                'team': team_name,
                'result': result,
                'search': search,
            }
        else:
            context = {
                'teams': teams,
                'team': team_name,
                'result': team_members,
                'search': "",
            }
        return render(request, 'user_manage.html', context)

    elif team_manager:
        superusers = User.objects.filter(is_superuser=True)
        superuser_ids = []
        for superuser in superusers.values():
            superuser_ids.append(superuser['id'])

        team = team_manager.team
        team_members = Profile.objects.filter(team=team).exclude(user__in=superuser_ids)

        if request.method == "POST":
            search = request.POST.get('search')

            result = team_members
            result = result.filter(name__icontains=search)

            context = {
                'team': team,
                'result': result,
                'search': search,
            }
        else:
            context = {
                'team': team,
                'result': team_members,
                'search': "",
            }
        return render(request, 'user_manage.html', context)
    else:
        return redirect('schedule-index')


@login_required
def manage_detail(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    team_manager = TeamManager.objects.filter(team=profile.team).filter(user=user).exists()
    if team_manager or user.is_superuser:
        member = Profile.objects.get(pk=pk)
        is_manager = TeamManager.objects.filter(user=member.user).exists()

        teams = Team.objects.all()
        positions = Position.objects.all()

        work_start_date = ""
        work_end_date = ""
        work_log = WorkLog.objects.filter(user=member.user)

        if request.method == "POST":
            work_start_date = request.POST.get('work_start_date')
            work_end_date = request.POST.get('work_end_date')

            if work_start_date:
                work_log = work_log.filter(create_time__date__gte=work_start_date)
            if work_end_date:
                work_log = work_log.filter(create_time__date__lte=work_end_date)

        last_work_log = work_log.order_by('-create_time').first()

        context = {
            'member': member,
            'is_manager': is_manager,
            'teams': teams,
            'positions': positions,
            'work_start_date': work_start_date,
            'work_end_date': work_end_date,
            'profile': MemberInfoForm(instance=member),
            'last_work_log': last_work_log,
        }
        return render(request, 'user_manage_detail.html', context)
    else:
        return redirect('schedule-index')


@login_required
def manage_delete(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    team_manager = TeamManager.objects.filter(team=profile.team).filter(user=user).first()
    if team_manager or user.is_superuser:
        member = Profile.objects.get(pk=pk)
        if member.currently_employed:
            member.currently_employed = False
        else:
            member.currently_employed = True
        member.save()
        return redirect('manage_detail', pk)
    else:
        return redirect('schedule-index')


@login_required
def manage_permit(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    team_manager = TeamManager.objects.filter(team=profile.team).filter(user=user).first()
    if team_manager or user.is_superuser:
        member = Profile.objects.get(pk=pk)
        is_manager = TeamManager.objects.filter(user=member.user).exists()

        if is_manager:
            permit = TeamManager.objects.filter(user=member.user)
            permit.delete()
        else:
            permit = TeamManager(user=member.user, team=member.team)
            permit.save()
        return redirect('manage_detail', pk)
    else:
        return redirect('schedule-index')


@login_required
def manage_position(request, pk, position_name):
    user = request.user
    profile = Profile.objects.get(user=user)
    team_manager = TeamManager.objects.filter(team=profile.team).filter(user=user).first()
    if team_manager or user.is_superuser:
        member = Profile.objects.get(pk=pk)
        position = Position.objects.get(name=position_name)
        member.position = position
        member.save()
        return JsonResponse("success", safe=False)
    return JsonResponse("fail", safe=False)


@login_required
def manage_team(request, pk, team_name):
    user = request.user
    profile = Profile.objects.get(user=user)
    team_manager = TeamManager.objects.filter(team=profile.team).filter(user=user).first()
    if team_manager or user.is_superuser:
        member = Profile.objects.get(pk=pk)
        is_manager = TeamManager.objects.filter(user=member.user).exists()
        if is_manager:
            permit = TeamManager.objects.filter(user=member.user)
            permit.delete()
        team = Team.objects.get(name=team_name)
        member.team = team
        member.save()
        return JsonResponse("success", safe=False)
    return JsonResponse("fail", safe=False)


# 일자 선택시 실 출퇴근 시간, 총 근무 시간 가져오는 api(시간은 반올림 된 형태로 출력 및 합산)
@login_required
def calc_work_hours(request):
    user = request.user
    member_pk = request.GET.get('member_pk')
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    profile = Profile.objects.get(user=user)
    team_manager = TeamManager.objects.filter(team=profile.team).filter(user=user).first()
    result = {}
    total_working_time = 0
    work_hours_list = []
    member = Profile.objects.get(pk=member_pk)
    work_hours = WorkHour.objects.filter(user=member.user)

    if start_date:
        work_hours = work_hours.filter(date__gte=start_date)
    if end_date:
        work_hours = work_hours.filter(date__lte=end_date)

    for work_hour in work_hours.values():
        work_hour_dict = {}
        work_hour_dict['date'] = work_hour['date']
        s_t = work_hour['start_time']
        arranged_start_time = datetime.datetime(s_t.year, s_t.month, s_t.day, s_t.hour, 10*(s_t.minute // 10))
        start_time = arranged_start_time.strftime("%H:%M")
        e_t = work_hour['end_time']
        if e_t:
            arranged_end_time = datetime.datetime(e_t.year, e_t.month, e_t.day, e_t.hour, 10 * (e_t.minute // 10))
            end_time = arranged_end_time.strftime("%H:%M")
            total_working_time += (arranged_end_time - arranged_start_time).seconds
        else:
            arranged_end_time = e_t
            end_time = ''

        work_hour_dict['start_time'] = start_time
        work_hour_dict['end_time'] = end_time
        work_hours_list.append(work_hour_dict)

    result['total_working_time'] = str(round(total_working_time/3600, 1)) + ' 시간 근무'
    result['work_hours_list'] = work_hours_list

    return JsonResponse(result, safe=False)


@login_required
def send_work_log(request, member_pk, date):
    user = request.user
    profile = Profile.objects.get(user=user)
    team_manager = TeamManager.objects.filter(team=profile.team).filter(user=user).first()
    member = Profile.objects.get(pk=member_pk)
    work_log = WorkLog.objects.filter(user=member.user).filter(create_time__date=date).first()
    if work_log:
        result = {
            'content': work_log.content,
            'create_time': work_log.create_time.strftime("%H:%M"),
        }
    else:
        result = {
            'content': '',
            'create_time': '',
        }
    return JsonResponse(result, safe=False)


@login_required
def manage_delete_real(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    team_manager = TeamManager.objects.filter(team=profile.team).filter(user=user).first()
    member = Profile.objects.get(pk=pk)
    if team_manager or user.is_superuser:
        if request.method == "POST":
            member_user = User.objects.get(pk=member.user.pk)
            member_user.delete()
            return redirect('manage_list')
        else:
            context = {
                'member': member,
            }
            return render(request, 'user_delete_confirm.html', context)
    else:
        return redirect('schedule-index')