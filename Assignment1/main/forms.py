from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from .models import Profile

class NewUserForm(UserCreationForm):
    #username = forms.CharField(label='username', max_length=320,widget=forms.TextInput(attrs={'class': 'form-control'}))
    #password1 = forms.CharField(label='password1', max_length=320,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    #password2 = forms.CharField(label='password2', max_length=320,widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class SaveLocationForm(forms.Form):

    class Meta:
        model = Profile
        fields = ('location',)

    def __init__(self, *args, **kwargs):
        coordinate = kwargs['data'].pop('coordinate', None)
        if coordinate:
            coordinate = coordinate.replace(',', '')  # remove comma, as we need single space between two numbers.
            kwargs['data']['coordinate'] = f'SRID=4326;POINT({coordinate})'

        super(SaveLocationForm, self).__init__(*args, **kwargs)