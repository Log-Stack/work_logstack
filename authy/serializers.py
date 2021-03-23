from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Team, Profile


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name','date']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user','team','positon','name','birth_day','phone_number','currently_employed']


