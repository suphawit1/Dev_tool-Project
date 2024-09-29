from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.db.models import Value, Count, F,Sum
from django.db.models.functions import Concat
from datetime import datetime
from report.forms import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import *
from django.contrib.contenttypes.models import ContentType


class Report(View):
    def get(self, request):
        return render('index.html') 
        
    def post(self, request):
        # <view logic>
        return redirect('index') 


class LoginView(View):
    
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'authentication/login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)

            if user is not None:
                login(request,user)
                return redirect('book')
            else:
                messages.error(request,'invalid username')
        else:
            messages.error(request,'invalid username')
        return render(request,'authentication/login.html', {'form':form})
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/login/')
    
class RegisterView(View):
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            my_user = form.save()
            print(my_user)
            Customer.objects.create(
                user = my_user,
                phone = my_user.phone,
                address = my_user.address
            )
            messages.success(request, 'Account created successfully')
            return redirect('login') 
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'authentication/register.html', {'form': form}) 

    def get(self, request):
        form = CustomUserCreationForm()
        context = {
            'form': form
        }
        return render(request, 'authentication/register.html', context)
    