from django.db import models
from django.contrib.auth.models import *


class Contact(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=500)

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete= models.PROTECT)
    contact = models.ForeignKey(Contact,on_delete = models.CASCADE)
    

class FallEvent(models.Model):
    user = models.CharField(max_length=100)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.user_id} - {self.timestamp}"