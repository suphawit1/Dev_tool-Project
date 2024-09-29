from django.urls import path

from . import views

urlpatterns = [
    path("index/",views.Report.as_view(), name ="index"),
    path("login/", views.LoginView.as_view(), name='login'),
    path("register/", views.RegisterView.as_view(), name='register'),
    path('logout', views.LogoutView.as_view(), name="logout"),
]