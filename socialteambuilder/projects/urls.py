# project urls.py

from django.urls import path, include
from . import views

app_name = 'projects'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
