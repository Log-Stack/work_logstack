from django import forms
from django.forms import SplitDateTimeWidget

from .models import WorkLog, WorkHour


class WorkLogForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'textarea is-primary', 'placeholder': 'Work Log input'}))

    class Meta:
        model = WorkLog
        fields = ('content',)


class WorkHourForm(forms.ModelForm):
    start_time = forms.SplitDateTimeField(
        widget=SplitDateTimeWidget(date_attrs={'type': 'hidden'}, time_attrs={'type': 'time'}, time_format='%H:%M:00'))
    end_time = forms.SplitDateTimeField(
        widget=SplitDateTimeWidget(date_attrs={'type': 'hidden'}, time_attrs={'type': 'time'}, time_format='%H:%M:00'))

    class Meta:
        model = WorkHour
        fields = ('start_time', 'end_time')
