from django import forms
from .models import Schedule, ToDo

from django.forms import ClearableFileInput


class NewScheduleWeekForm(forms.ModelForm):
    week_start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': "input", 'type': "date", 'id': 'week_start_date'}))

    sun_work_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select is-success work_type'}),
                                      choices=Schedule.WORK_TYPES)
    sun_start = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input start_time", 'type': "time"}), required=False)
    sun_end = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input end_time", 'type': "time"}), required=False)

    mon_work_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select is-success work_type'}),
                                      choices=Schedule.WORK_TYPES)
    mon_start = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input start_time", 'type': "time"}), required=False)
    mon_end = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input end_time", 'type': "time"}), required=False)

    tue_work_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select is-success work_type'}),
                                      choices=Schedule.WORK_TYPES)
    tue_start = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input start_time", 'type': "time"}), required=False)
    tue_end = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input end_time", 'type': "time"}), required=False)

    wed_work_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select is-success work_type'}),
                                      choices=Schedule.WORK_TYPES)
    wed_start = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input start_time", 'type': "time"}), required=False)
    wed_end = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input end_time", 'type': "time"}), required=False)

    thu_work_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select is-success work_type'}),
                                      choices=Schedule.WORK_TYPES)
    thu_start = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input start_time", 'type': "time"}), required=False)
    thu_end = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input end_time", 'type': "time"}), required=False)

    fri_work_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select is-success work_type'}),
                                      choices=Schedule.WORK_TYPES)
    fri_start = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input start_time", 'type': "time"}), required=False)
    fri_end = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input end_time", 'type': "time"}), required=False)

    sat_work_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select is-success work_type'}),
                                      choices=Schedule.WORK_TYPES)
    sat_start = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input start_time", 'type': "time"}), required=False)
    sat_end = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input end_time", 'type': "time"}), required=False)

    class Meta:
        model = Schedule
        fields = ('week_start_date',

                  'sun_work_type',
                  'sun_start',
                  'sun_end',

                  'mon_work_type',
                  'mon_start',
                  'mon_end',

                  'tue_work_type',
                  'tue_start',
                  'tue_end',

                  'wed_work_type',
                  'wed_start',
                  'wed_end',

                  'thu_work_type',
                  'thu_start',
                  'thu_end',

                  'fri_work_type',
                  'fri_start',
                  'fri_end',

                  'sat_work_type',
                  'sat_start',
                  'sat_end')


class NewScheduleDayForm(forms.ModelForm):
    week_start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': "input", 'type': "date", 'id': 'week_start_date'}))

    work_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select is-success work_type'}),
                                      choices=Schedule.WORK_TYPES)
    start = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input start_time", 'type': "time"}), required=False)
    end = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input end_time", 'type': "time"}), required=False)

    class Meta:
        model = Schedule
        fields = ('week_start_date',

                  'work_type',
                  'start',
                  'end',

                  )
