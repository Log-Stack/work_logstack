from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)


class Position(models.Model):
    name = models.CharField(max_length=26)


class TeamManager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL)

    name = models.CharField(max_length=25)
    birth_day = models.DateField()
    phone_number = models.CharField(max_length=50)
    currently_employed = models.BooleanField(default=True)

