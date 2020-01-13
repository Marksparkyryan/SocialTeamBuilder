# project urls.py

from django.urls import path, include
from . import views

app_name = 'projects'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('applications/<category>/<q>/', views.ApplicationsList.as_view(), name='applications'),
    path('ajax/update_app_status/', views.update_app_status, name='update_app_status'),
]
