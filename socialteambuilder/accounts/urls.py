# accounts/urls.py

from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.Register.as_view(), name="register"),
    path('activate/<int:pk>/<slug:token>/', views.Activate.as_view(), name="activate"),
    path('updateuser/', views.update_user, name="updateuser"),
    path('profile/', views.Profile.as_view(), name="profile"),
]