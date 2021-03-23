from django import forms
from .models import Schedule

from django.forms import ClearableFileInput


class NewScheduleForm(forms.ModelForm):
    week_start_date = forms.DateField()

    sun_work_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select is-success'}),
                                      choices=Schedule.WORK_TYPES)
    sun_start = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input", 'type': "time"}))
    sun_end = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input", 'type': "time"}))

    mon_work_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select is-success'}),
                                      choices=Schedule.WORK_TYPES)
    mon_start = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input", 'type': "time"}))
    mon_end = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input", 'type': "time"}))

    tue_work_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select is-success'}),
                                      choices=Schedule.WORK_TYPES)
    tue_start = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input", 'type': "time"}))
    tue_end = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input", 'type': "time"}))

    wed_work_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select is-success'}),
                                      choices=Schedule.WORK_TYPES)
    wed_start = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input", 'type': "time"}))
    wed_end = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input", 'type': "time"}))

    thu_work_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select is-success'}),
                                      choices=Schedule.WORK_TYPES)
    thu_start = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input", 'type': "time"}))
    thu_end = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input", 'type': "time"}))

    fri_work_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select is-success'}),
                                      choices=Schedule.WORK_TYPES)
    fri_start = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input", 'type': "time"}))
    fri_end = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input", 'type': "time"}))

    sat_work_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'select is-success'}),
                                      choices=Schedule.WORK_TYPES)
    sat_start = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input", 'type': "time"}))
    sat_end = forms.TimeField(widget=forms.TimeInput(attrs={'class': "input", 'type': "time"}))

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
