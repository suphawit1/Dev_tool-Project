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
from twilio.rest import Client
from twilio.base.exceptions import TwilioException


class Report(View):
    def get(self, request):
        return render(request,'index.html') 
    
class ReportAction(View):
    def post(self, request):
        def post(self, request):
            account_sid = "AC0532f2d9baff64b18157f6b4275f9ef6"
            auth_token = "066eadfda920854dc12d9f0856e29bf1"
            client = Client(account_sid, auth_token)

            # The number you want to send the SMS to
            to_number = "+66995610396"  # Change this to the recipient's number
            from_number = "+19032283644"  # Your Twilio number

            try:
                # Send the SMS
                message = client.messages.create(
                    body="This is your message content!",  # Customize the message content
                    from_=from_number,
                    to=to_number
                )

                return HttpResponse(f"SMS sent with SID: {message.sid}")  # Return the SID of the sent message
            except TwilioException as e:
                return HttpResponse(f"Failed to send SMS: {str(e)}", status=500)


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
                return redirect('index')
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
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            Customer.objects.create(
                user = my_user,
                phone = phone,
                address = address,
                contact=None
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
    