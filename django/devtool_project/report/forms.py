from django import forms
from django.contrib.auth.models import User
from .models import *
from datetime import date
from django.forms import ModelForm,DateInput
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=30, required=True, help_text='Required')
    address = forms.CharField(max_length=30, required=True, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'phone', 'address', 'password1', 'password2')