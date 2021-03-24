from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authy.forms import TeamCreateForm, UserCreateForm, ProfileForm
from authy.models import Team, Profile
from authy.serializers import TeamSerializer, ProfileSerializer

from authy.models import TeamManager, Position
from work_log.models import WorkHour


@login_required
def index(request):
    user = request.user

    template = loader.get_template('index.html')

    context = {
        'user': user,
    }

    return HttpResponse(template.render(context, request))



# Leader of team creates staff's account
@login_required
def CreateUserView(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()

            print("ok")
            return redirect('index')
        else:
            print("not ok")
    else:
        form = TeamCreateForm()

    context = {
        'form': form,
    }

    return render(request, 'user_create.html')


# Leader of team creates team
@login_required
def CreateTeamView(request):
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
    }

    return render(request, 'team_create.html', context)


#Staff edits profile
def EditProfileView(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            # obj.name = form.cleaned_data.get('name')
            # obj.birth_day = form.cleaned_data.get('birth_day')
            # obj.phone_number = form.cleaned_data.get('phone_number')
            # obj.user.email = form.cleaned_data.get('email_address')
            # print(request.user)
            user = User.objects.get(username=request.user)
            user.email = form.cleaned_data.get('email_address')
            user.save()
            obj.save()
            return redirect('index')
        else:
            print("not ok")
            print(form.errors)
    else:
        print("not POST")
        form = ProfileForm()

    context = {
        'id' : request.user.username,
        'form': form,
    }
    return render(request, 'user_info_edit.html', context)





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
@login_required
def manage_list(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    team_manager = TeamManager.objects.filter(team=profile.team).filter(user=user).first()
    if team_manager:
        team = team_manager.team
        team_members = Profile.objects.filter(team=team)

        if request.method == "POST":
            member = request.POST.get('member')
            search = request.POST.get('search')

            result = team_members
            if member != 'all':
                result = team_members.filter(name=member)
            result = result.filter(name__icontains=search)

            context = {
                'team': team,
                'team_members': team_members,
                'result': result,
                'member': member,
                'search': search,
            }
        else:
            context = {
                'team': team,
                'team_members': team_members,
                'result': team_members,
                'member': "",
                'search': "",
            }
        return render(request, 'user_manage.html', context)
    else:
        return redirect('index')


@login_required
def manage_detail(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    team_manager = TeamManager.objects.filter(team=profile.team).filter(user=user).exists()
    if team_manager:
        member = Profile.objects.get(pk=pk)
        is_manager = TeamManager.objects.filter(user=member.user).exists()

        teams = Team.objects.all()
        positions = Position.objects.all()

        start_date = ""
        end_date = ""
        work_hours = WorkHour.objects.filter(user=member.user)

        if request.method == "POST":
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            if start_date:
                work_hours = work_hours.filter(date__gte=start_date)
            if end_date:
                work_hours = work_hours.filter(date__lte=end_date)
            context = {
                'member': member,
                'is_manager': is_manager,
                'teams': teams,
                'positions': positions,
                'start_date': start_date,
                'end_date': end_date,
                'work_hours': work_hours.order_by('-date'),
            }
        else:
            context = {
                'member': member,
                'is_manager': is_manager,
                'teams': teams,
                'positions': positions,
                'start_date': start_date,
                'end_date': end_date,
                'work_hours': work_hours.order_by('-date'),
            }
        return render(request, 'user_manage_detail.html', context)
    else:
        return redirect('index')


@login_required
def manage_delete(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    team_manager = TeamManager.objects.filter(team=profile.team).filter(user=user).first()
    if team_manager:
        member = Profile.objects.get(pk=pk)
        if member.currently_employed:
            member.currently_employed = False
        else:
            member.currently_employed = True
        member.save()
        return redirect('manage_detail', pk)
    else:
        return redirect('index')


@login_required
def manage_permit(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    team_manager = TeamManager.objects.filter(team=profile.team).filter(user=user).first()
    if team_manager:
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
        return redirect('index')


@login_required
def manage_position(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    team_manager = TeamManager.objects.filter(team=profile.team).filter(user=user).first()
    if team_manager:
        if request.method == "POST":
            member = Profile.objects.get(pk=pk)
            position = request.POST.get('position')
            position = Position.objects.get(name=position)
            member.position = position
            member.save()
            return redirect('manage_detail', pk)
    return redirect('index')


@login_required
def manage_team(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    team_manager = TeamManager.objects.filter(team=profile.team).filter(user=user).first()
    if team_manager:
        if request.method == "POST":
            member = Profile.objects.get(pk=pk)
            is_manager = TeamManager.objects.filter(user=member.user).exists()
            if is_manager:
                permit = TeamManager.objects.filter(user=member.user)
                permit.delete()
            team = request.POST.get('team')
            team = Team.objects.get(name=team)
            member.team = team
            member.save()
            return redirect('manage_detail', pk)
    return redirect('index')