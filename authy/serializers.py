from rest_framework import serializers
from .models import Team, Profile


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id','name','date']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['team','position','name','birth_day','phone_number','currently_employed']


