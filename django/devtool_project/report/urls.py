from django.urls import path

from . import views

urlpatterns = [
    path("report-fall/",views.Report.as_view(), name ="report"),
]