from django import forms
from django.db import models

from authy.models import Team


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',)
