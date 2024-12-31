from django.urls import path
from report.views import Report
from . import views

urlpatterns = [
    path("index/",views.Report.as_view(), name ="index"),
    path("sensor/",views.SensorView.as_view(), name ="sensor"),
    path("report/",views.ReportAction.as_view(), name ="report"),
    path("login/", views.LoginView.as_view(), name='login'),
    path("register/", views.RegisterView.as_view(), name='register'),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='profile'),
    path('edit-profile/<int:user_id>/', views.EditProfileView.as_view(), name='edit-profile'),
    path('add-contact/<int:user_id>/', views.AddEditContactView.as_view(), name='add-contact'),
    path('edit-contact/<int:user_id>/<int:contact_id>/', views.AddEditContactView.as_view(), name='edit-contact'),

]
