from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.template import loader
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from authy.forms import TeamCreateForm, UserCreateForm, ProfileForm, SignupForm, ChangePasswordForm
from authy.models import Team, Profile
from authy.serializers import TeamSerializer, ProfileSerializer


@login_required
def index(request):
    user = request.user

    template = loader.get_template('index.html')

    context = {
        'user': user,
    }

    return HttpResponse(template.render(context, request))


@login_required
def CreateUserView(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        # team_form = TeamForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, password=password)

            #user = form.save()

            team_name = form.cleaned_data.get('name')
            team = Team.objects.get(name=team_name)
            profile = Profile(user=user, team=team)
            profile.save()
            print(profile)
            return redirect('index')
    else:
        form = SignupForm()

    context = {
        'form': form,
    }

    return render(request, 'user_create.html', context)


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


# @login_required
# def UserDetailView(request, user_id):
#     profile = get_object_or_404(Profile, user_id=user_id)
#     context = {
#         'profile': profile
#     }
#
#     return render(request,'user_search_result.html',context)

@login_required
def ProfileView(request):
    user_id = request.user.id
    profile = get_object_or_404(Profile, user_id=user_id)
    context = {
        'profile': profile
    }

    return render(request,'user_info.html', context)


# Staff edits profile
#   fields = ['name', 'birth_day', 'phone_number', 'email_address']
def EditProfileView(request):
    user = request.user
    profile = Profile.objects.filter(user=user)[0]


    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
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

        #Pagination
        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        context = {
            'users': users_paginator
        }
    template = loader.get_template('user_search.html')


    return HttpResponse(template.render(context, request))


@login_required
def SearchSelectView(request):
    return render(request,'user_search_result.html')


@login_required
def UserDetailView(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    context = {
        'profile': profile
    }

    return render(request,'user_search_result.html',context)


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
