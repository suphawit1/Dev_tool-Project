from django.urls import path

from . import views

urlpatterns = [
    path("index/",views.Report.as_view(), name ="index"),
]