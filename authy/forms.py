from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from authy.models import Team, Profile, Position
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        profile = Profile.objects.get(user=user)
        if not profile.currently_employed:
            raise forms.ValidationError('There was a problem with your login.', code='invalid_login')


class MemberInfoForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['birth_day', 'phone_number', 'email_address', 'start_date']
        widgets = {
            'email_address': forms.TextInput(attrs={'type': "text", 'class': 'input is-dark'}),
            'phone_number': forms.TextInput(attrs={'type': "text", 'class': 'input is-dark'}),
            'start_date': forms.DateInput(attrs={'type': "date", 'class': 'input is-dark'}),
            'birth_day': forms.DateInput(attrs={'type': "date", 'class': 'input is-dark'}),
        }





class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',)


class PositionCreateForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('name',)


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password',)


class ProfileForm(forms.ModelForm):
    picture = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['picture', 'name', 'birth_day', 'phone_number', 'email_address', 'start_date']


class ForbiddenUsers(object):
    pass


class InvalidUser(object):
    pass


class UniqueUser(object):
    pass


# class SignupForm(forms.ModelForm):
#     # django form widget
#     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium'}), max_length=30,
#                                required=True, )
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}))
#     confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), required=True,
#                                        label="Confirm your password.")
#
#     class Meta:
#         model = User
#         fields = ('username', 'password')
#
#     def __init__(self, *args, **kwargs):
#         super(SignupForm, self).__init__(*args, **kwargs)
#
#     # self.fields['username'].validators.append(ForbiddenUsers)
#     # self.fields['username'].validators.append(InvalidUser)
#     # self.fields['username'].validators.append(UniqueUser)
#     # self.fields['email'].validators.append(UniqueEmail)
#
#     def clean(self):
#         super(SignupForm, self).clean()
#         password = self.cleaned_data.get('password')
#         confirm_password = self.cleaned_data.get('confirm_password')
#
#         if password != confirm_password:
#             self._errors['password'] = self.error_class(['Passwords do not match. Try again'])
#         return self.cleaned_data
#
#
# class TeamForm(forms.ModelForm):
#     class Meta:
#         model = Team
#         fields = ('name',)

def SetPassword():
    password = "logstack"
    return password



class SignupForm(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium'}), max_length=30,
                               required=True, )
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium', 'value':'logstack'}))
    # confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), required=True,
    #                                    label="Confirm your password.")


    class Meta:
        model = User
        fields = ('username', )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

    # def clean(self):
    #     super(SignupForm, self).clean()
    #     password = self.cleaned_data.get('password')
    #     #confirm_password = self.cleaned_data.get('confirm_password')
    #
    #     #if password != confirm_password:
    #     #    self._errors['password'] = self.error_class(['Passwords do not match. Try again'])
    #     return self.cleaned_data


class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="Old password",
                                   required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), label="New password",
                                   required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}),
                                       label="Confirm new password", required=True)

    class Meta:
        model = User
        fields = ('id', 'old_password', 'new_password', 'confirm_password')

    def clean(self):
        super(ChangePasswordForm, self).clean()
        id = self.cleaned_data.get('id')
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors['old_password'] = self.error_class(['Old password do not match.'])
        if new_password != confirm_password:
            self._errors['new_password'] = self.error_class(['Passwords do not match.'])
        return self.cleaned_data
