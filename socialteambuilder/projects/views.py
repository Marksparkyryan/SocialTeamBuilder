# projects/views

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, UpdateView
from django.utils.text import slugify

from .models import Application

User = get_user_model()


class DashboardView(TemplateView):
    template_name = 'projects/dashboard.html'


class ApplicationsList(LoginRequiredMixin, ListView):
    model = Application

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            Q(position__project__owner=self.request.user) |
            Q(user_id=self.request.user)
        )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs['category']
        q = self.kwargs['q']
        if q != 'all':
            if category == 'status':
                filtered = self.get_queryset().filter(
                    status__icontains=q
                )
            elif category == 'project':
                filtered =  self.get_queryset().filter(
                    position__project__slug=q
                )
            elif category == 'need':
                filtered =  self.get_queryset().filter(
                    position__slug=q
                )
        else:
            filtered = self.get_queryset()
        
        context['q'] = self.kwargs['q']
        context['filtered'] = filtered
        return context




@login_required
def update_app_status(request):
    pk = request.GET.get('app_pk', None)
    status = request.GET.get('status', None)

    try:
        app = Application.objects.get(id=pk)
        app.status = status
        app.save()
        data = {
            'updated': True
        }
    except Application.DoesNotExists as err:
        data = {
            'updated': False,
            'error': err
        }
    finally:
        return JsonResponse(data)
