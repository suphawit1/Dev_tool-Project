from django.http import HttpResponse
from django.views import View


class Report(View):
    def get(self, request):
        # <view logic>
        return HttpResponse(status=201)
    
    def post(self, request):
        # <view logic>
        return HttpResponse(status=201)