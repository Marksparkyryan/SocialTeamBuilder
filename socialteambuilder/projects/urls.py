# project urls.py

from django.urls import path, include
from . import views

app_name = 'projects'

urlpatterns = [
    path('dashboard/<category>/<q>/', views.DashboardView.as_view(), name='dashboard'),
    path('applications/<box>/<category>/<q>/', views.ApplicationsList.as_view(), name='applications'),
    path('ajax/update_app_status/', views.UpdateAppStatus.as_view(), name='update_app_status'),
    path('ajax/create_app/', views.CreateApp.as_view(), name='newapp'),
    path('project/<slug>/', views.ProjectView.as_view(), name='project'),
    path('create-project/', views.create_project, name="create_project"),
]
