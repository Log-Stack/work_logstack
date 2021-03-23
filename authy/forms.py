from django import forms
from django.contrib.auth.models import User
from django.db import models

from authy.models import Team, Profile


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',)


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password',)




class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['name','birth_day','phone_number','email_address']
