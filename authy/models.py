from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=26)

    def __str__(self):
        return self.name


class TeamManager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # blank = True 추가
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True)
    # blank = True 추가
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, blank=True, null=True)

    name = models.CharField(max_length=25)
    birth_day = models.DateField()
    # null=True
    phone_number = models.CharField(max_length=50,null=True)
    email_address = models.CharField(max_length=100,default="")
    currently_employed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.team} - {self.name}"

