# projects/views

from braces.views import PrefetchRelatedMixin

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic import TemplateView, UpdateView, View, DetailView
from django.views.generic.list import ListView
from django.views.generic.detail import SingleObjectMixin
from django.utils.text import slugify

from .models import Application, Project

User = get_user_model()


class CustomLoginRequired(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        apps = Application.objects.filter(
            user=request.user,
            unread=True,
        )
        if apps.exists():
            for app in apps:
                messages.success(request, "You've been {} for the position of {}, {}.".format(app.get_status_display().lower(), app.position.title, app.position.project.title))
                app.unread = False
                app.save()
        return super().dispatch(request, *args, **kwargs)


class DashboardView(CustomLoginRequired, PrefetchRelatedMixin, ListView):
    queryset = Project.objects.all()
    template_name = 'projects/dashboard.html'
    prefetch_related = ['position_set',]
    paginate_by = 2

    def get_queryset(self, *args, **kwargs):
        super().get_queryset(*args, **kwargs)
        # get distinct projects that are currently open and have empty positions
        queryset = self.queryset.filter(
            status='A',
            position__status='E' 
        ).distinct()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs['category']
        q = self.kwargs['q']
        if q != 'all':
            if category == 'need':
                filtered =  self.get_queryset().filter(
                    position__slug=q
                )
            if category == 'skill':
                filtered = self.get_queryset().filter(
                    position__skills__name=q
                )       
            if category == 'skills':
                filtered = self.get_queryset().filter(
                    position__skills__in=self.request.user.skills.all()
                )             
        else:
            filtered = self.get_queryset()

        context['q'] = self.kwargs['q']
        context['filtered'] = filtered
        return context


class ApplicationsList(CustomLoginRequired, ListView):
    model = Application
    paginate_by = 2

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs) 
        queryset = queryset = queryset.filter(
            Q(position__project__owner=self.request.user) |
            Q(user=self.request.user)
        ).distinct()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        box = self.kwargs['box']
        if box == 'inbox':
            filtered = self.get_queryset().filter(
                position__project__owner=self.request.user
            )
        else:
            filtered = self.get_queryset().filter(
                user=self.request.user
            )
        category = self.kwargs['category']
        q = self.kwargs['q']
        if q != 'all':
            if category == 'status':
                filtered = filtered.filter(
                    status__icontains=q
                )
            elif category == 'project':
                filtered =  filtered.filter(
                    position__project__slug=q
                )
            elif category == 'need':
                filtered =  filtered.filter(
                    position__slug=q
                )
        
        context['q'] = self.kwargs['q']
        context['box'] = self.kwargs['box']
        context['filtered'] = filtered
        context['inbox_count'] = self.get_queryset().filter(
            status='U',
            position__project__owner=self.request.user
        ).count()
        return context
      

class UpdateAppStatus(CustomLoginRequired, View):
    http_method_names = ['post',]

    def post(self, request, *args, **kwargs):
        print(request.POST)
        pk = self.request.POST.get('app_pk')
        status = self.request.POST.get('status')
        user = self.request.user 
        print(pk, status, user)
        app = get_object_or_404(Application, pk=pk)
        if user == app.position.project.owner:
            if status in ('A', 'R'):
                app.status = status
                app.unread = True
                app.save()
                data = {
                    'updated': True,
                    'new_status': app.get_status_display()
                }
                return JsonResponse(data)
            return HttpResponseBadRequest()
        raise PermissionDenied


class ProjectView(DetailView):
    model = Project
    template_name = 'projects/project.html'



