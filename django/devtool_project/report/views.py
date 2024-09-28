from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect


class Report(View):
    def get(self, request):
        return render('index.html') 
        
    def post(self, request):
        # <view logic>
        return redirect('index') 
