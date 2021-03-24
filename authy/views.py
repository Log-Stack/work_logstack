from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
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
        if form.is_valid():
            username = form.cleaned_data.get('username')

            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password)
            return redirect('index')
    else:
        form = SignupForm()

    context = {
        'form': form,
    }

    return render(request, 'user_create.html', context)

#Leader of team creates staff's account
# @login_required
# def CreateUserView(request):
#     if request.method == 'POST':
#         form = UserCreateForm(request.POST)
#         if form.is_valid():
#             form.save()
#
#
#             print("ok")
#             return redirect('index')
#         else:
#             print("not ok")
#     else:
#         form = TeamCreateForm()
#
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'user_create.html')

# @login_required
# def CreateUserView(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # username = form.cleaned_data.get('username')
#             # raw_password = form.cleaned_data.get('password1')
#             # User.objects.create_user(username=username, password=raw_password)
#             #login(request, user)
#             return redirect('index')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'user_create.html', {'form': form})


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
