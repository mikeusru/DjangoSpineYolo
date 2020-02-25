from django import forms
from django.contrib.auth.models import User

from registration.models import UserProfileInfo


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class UserProfileInfoForm(forms.ModelForm):
    institute = forms.CharField(max_length=255)

    class Meta:
        model = UserProfileInfo
        fields = ('institute',)
