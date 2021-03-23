from django import forms
from .models import WorkLog


class WorkLogForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea is-primary', 'placeholder': 'Work Log input'}))

    class Meta:
        model = WorkLog
        fields = ('content',)

