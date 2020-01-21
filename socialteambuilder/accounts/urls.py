# accounts/urls.py

from django.urls import path, re_path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.Register.as_view(), name="register"),
    path('check-inbox/', views.CheckInbox.as_view(), name="check_inbox"),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    path('updateuser/', views.update_user, name="updateuser"),
    path('profile/<int:pk>/', views.Profile.as_view(), name="profile"),
]
