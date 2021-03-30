import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


def user_directory_path(instance, filename):
    # this file will be uploaded to MEDIA_ROOT /user(id)/filename
    profile_pic_name = 'user_{0}/profile.jpg'.format(instance.user.id)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_pic_name


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
    # blank,null=True (name, birth_day)
    name = models.CharField(max_length=25, blank=True, null=True)
    birth_day = models.DateField(blank=True, null=True)
    # blank,null=True (phone_number, email_address)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    email_address = models.CharField(max_length=100, blank=True, default="")
    currently_employed = models.BooleanField(default=True)
    picture = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name='Picture')
    start_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.team} - {self.user}"
