# project urls.py

from django.urls import path, include, re_path
from . import views

app_name = 'projects'

urlpatterns = [
    path('search/', views.SearchBar.as_view(), name='searchbar'),
    path('dashboard/<category>/<q>/', views.DashboardView.as_view(), name='dashboard'),
    path('applications/<box>/<category>/<q>/', views.ApplicationsList.as_view(), name='applications'),
    path('ajax/update_app_status/', views.UpdateAppStatus.as_view(), name='update_app_status'),
    path('ajax/create_app/', views.CreateApp.as_view(), name='newapp'),
    path('detail/<slug>/', views.ProjectView.as_view(), name='project'),
    re_path(r'^create-update-project/(?:(?P<slug>[-a-zA-Z0-9]+)/)?$', views.create_update_project, name="create_update_project"),
]
