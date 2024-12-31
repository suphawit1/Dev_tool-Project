from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
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
from report.models import *
from django.contrib import messages


class Report(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request):
        fall = FallEvent.objects.filter(user=request.user.username)
        context ={
            "fall_data":fall
        }
        return render(request,'index.html',context)

class SensorView(View):
    def get(self, request):
        return render(request,'sensor.html')
    
class ReportAction(LoginRequiredMixin, View):
    login_url = '/login/'
    api = TwilioAPI.objects.first()
    
    def post(self, request):
        api = TwilioAPI.objects.first()
        account_sid = api.account_sid
        auth_token = api.auth_token
        client = Client(account_sid, auth_token)

        to_number = request.user.customer.phone
        from_number = api.tel

        try:
            client.messages.create(
                body="ตรวจพบการล้ม",
                from_=from_number,
                to=to_number
            )
            messages.success(request, "ทำการแจ้งเตือนการล้ม")

            alpha = request.POST.get("alpha")
            beta = request.POST.get("beta")
            gamma = request.POST.get("gamma")
            accelerationX = request.POST.get("accelerationX")
            accelerationY = request.POST.get("accelerationY")
            accelerationZ = request.POST.get("accelerationZ")
            magnitude = request.POST.get("magnitude")

            # Check if any of the required fields are missing or empty
            if not all([alpha, beta, gamma, accelerationX, accelerationY, accelerationZ, magnitude]):
                sensors = None
            
            else:
                sensors = Sensor(
                    alpha=alpha,
                    beta=beta,
                    gamma=gamma,
                    accelerationX=accelerationX,
                    accelerationY=accelerationY,
                    accelerationZ=accelerationZ,
                    magnitude=magnitude
                )
                sensors.save()
            fall = FallEvent(
                user = request.user,
                timestamp = datetime.now(),
                sensor = sensors
            )
            fall.save()
        except TwilioException as e:
            messages.error(request, f"Failed to send SMS: {str(e)}")  # Store error message

        referer = request.META.get('HTTP_REFERER', '/')
        return redirect(referer)


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
    
class UserProfileView(View):
    def get(self, request,user_id):
        customer = Customer.objects.get(pk=user_id)
        context = {
            'customer' : customer
        }
        # เรนเดอร์เทมเพลตพร้อมกับส่ง context ไป
        return render(request, 'profile.html',context)
    
class EditProfileView(View):
    def get(self, request,user_id):
        # ดึงข้อมูลของ Member ที่เกี่ยวข้องกับผู้ใช้ที่ล็อกอินอยู่
        my_user = User.objects.get(pk=user_id)
        customer_instance = Customer.objects.get(user=my_user)
        form = UserProfileForm(instance=customer_instance, user=request.user)
        return render(request, 'edit_profile.html', {'form': form,'header_text': 'Edit Profile'} )

    def post(self, request,user_id):
        my_user = User.objects.get(pk=user_id)
        customer_instance = Customer.objects.get(user=my_user)
        form = UserProfileForm(request.POST, instance=customer_instance, user=my_user)
        if form.is_valid():
            form.save()
        return redirect(reverse('profile', args=[request.user.id]) )
    

class AddEditContactView(View):
    def get(self, request, user_id, contact_id=None):
        my_user = User.objects.get(pk=user_id)
        customer_instance = Customer.objects.get(user=my_user)

        if contact_id:
            contact_instance = get_object_or_404(Contact, id=contact_id, customer=customer_instance)
            form = ContactForm(instance=contact_instance)
            header_text = 'Edit Contact'
        else:
            form = ContactForm()
            header_text = 'Add Contact'

        return render(request, 'edit_profile.html', {'form': form, 'header_text': header_text})

    def post(self, request, user_id, contact_id=None):
        my_user = User.objects.get(pk=user_id)
        customer_instance = Customer.objects.get(user=my_user)

        # If contact_id is provided, we are editing an existing contact
        if contact_id:
            contact_instance = get_object_or_404(Contact, id=contact_id, customer=customer_instance)
            form = ContactForm(request.POST, instance=contact_instance)
            header_text = 'Edit Contact'
        else:
            # Otherwise, we are adding a new contact
            form = ContactForm(request.POST)
            header_text = 'Add Contact'

        if form.is_valid():
            contact_instance = form.save(commit=False)
            contact_instance.customer = customer_instance  # Associate the contact with the customer
            contact_instance.save()

            return redirect(reverse('profile', args=[request.user.id]))

        return render(request, 'edit_profile.html', {'form': form, 'header_text': header_text})

    







    
# class AddContactView(View):
#     def get(self, request, user_id):
#         my_user = User.objects.get(pk=user_id)
#         customer_instance = Customer.objects.get(user=my_user)

#         if customer_instance.contact:
#             form = ContactForm(instance=customer_instance.contact)
#             header_text = 'Edit Contact'
#         else:
#             form = ContactForm()
#             header_text = 'Add Contact'

#         return render(request, 'edit_profile.html', {'form': form, 'header_text' : header_text})

#     def post(self, request, user_id):
#         my_user = User.objects.get(pk=user_id)
#         customer_instance = Customer.objects.get(user=my_user)

#         if customer_instance.contact:
#             form = ContactForm(request.POST, instance=customer_instance.contact)
#             header_text = 'Edit Contact'
#         else:
#             form = ContactForm(request.POST)
#             header_text = 'Add Contact'

#         if form.is_valid():
#             contact_instance = form.save()

#             customer_instance.contact = contact_instance
#             customer_instance.save()

#             return redirect(reverse('profile', args=[request.user.id]))

#         return render(request, 'edit_profile.html', {'form': form,'header_text' : header_text})

