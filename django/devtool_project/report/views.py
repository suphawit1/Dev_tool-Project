from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect


class Report(View):
    def get(self, request):
        return render(request,'index.html') 
    
class ReportAction(View):
    def post(self, request):
        # <view logic>
        return redirect('index') 
