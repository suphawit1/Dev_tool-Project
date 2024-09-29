from django.urls import path
from report.views import Report
from . import views

urlpatterns = [
    path("index/",views.Report.as_view(), name ="index"),
]