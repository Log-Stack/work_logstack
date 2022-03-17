from django.db import models
from django.utils import timezone


class Person(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    image = models.ImageField()
    file = models.FileField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f'{self.name}, {self.phone}, {self.email}, {self.year}'


class Hit(models.Model):
    count = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)
