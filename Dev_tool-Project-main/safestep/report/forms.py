from django import forms
from django.contrib.auth.models import User
from .models import *
from datetime import date
from django.forms import ModelForm,DateInput
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, help_text='Required')
    last_name = forms.CharField(max_length=100, required=True, help_text='Required')
    phone = forms.CharField(max_length=30, required=True, help_text='Required')
    address = forms.CharField(max_length=30, required=True, help_text='Required')
    email = forms.CharField(max_length=30, required=True, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','phone', 'address','email', 'password1', 'password2')


class UserProfileForm(ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone','address'] 
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
        

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        member = super(UserProfileForm, self).save(commit=False)
        user = member.user  # Get the associated User object
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()  
            member.save()  
        return member
    
from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

