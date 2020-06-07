# projects/views

from braces.views import PrefetchRelatedMixin

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    HttpResponseRedirect
)
from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, DeleteView, CreateView
from django.views.generic.list import ListView

from .models import Application, Project, Position
from .forms import CreateProjectForm, PositionFormset, SearchBarForm

User = get_user_model()


class CustomLoginRequired(LoginRequiredMixin):
    """Custom mixin that inherits LoginRequiredMixin funcitonality but
    also overlays a pending message delivery feature.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        apps = Application.objects.filter(
            user=request.user,
            unread=True,
        )
        if apps.exists():
            for app in apps:
                messages.success(
                    request,
                    "You've been {} for the position of {}, {}.".format(
                        app.get_status_display().lower(),
                        app.position.title,
                        app.position.project.title
                    ))
                app.unread = False
                app.save()
        return super().dispatch(request, *args, **kwargs)


class DashboardView(CustomLoginRequired, ListView):
    """View for all open projects
    """
    queryset = Project.objects.all()
    template_name = 'projects/dashboard.html'

    def get_queryset(self, *args, **kwargs):
        """get distinct projects that are currently open and have empty
        positions
        """
        super().get_queryset(*args, **kwargs)
        queryset = self.queryset.filter(
            status='A',
            position__status='E'
        ).prefetch_related(
            'position_set'
        ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs['category']
        q = self.kwargs['q']
        if q != 'all':
            if category == 'need':
                filtered = self.get_queryset().filter(
                    position__slug=q
                )
            elif category == 'skill':
                filtered = self.get_queryset().filter(
                    position__skills__name=q
                )
            elif category == 'skills':
                not_user_positions = Position.objects.exclude(
                    applications__user=self.request.user
                )
                filtered = self.get_queryset().filter(
                    Q(position__skills__in=self.request.user.skills.all()) &
                    Q(position__in=[position for position in not_user_positions])
                )
            elif category == 'my-opps':
                not_user_positions = Position.objects.exclude(
                    applications__user=self.request.user
                )
                filtered = self.get_queryset().filter(
                    position__in=[position for position in not_user_positions]
                )
            elif category == 'accepted':
                filtered = self.get_queryset().filter(
                    Q(position__applications__user=self.request.user) &
                    Q(position__applications__status='R')
                )

        else:
            filtered = self.get_queryset()

        context['searchform'] = SearchBarForm()
        context['q'] = self.kwargs['q']
        context['filtered'] = filtered
        return context


class SearchBar(ListView):
    """View that handles queries submitted by the SearchForm
    """
    queryset = Project.objects.all()
    template_name = 'projects/dashboard.html'

    def get_queryset(self, *args, **kwargs):
        """get distinct projects that are currently open and have empty
        positions
        """
        super().get_queryset(*args, **kwargs)
        queryset = self.queryset.filter(
            status='A',
            position__status='E'
        ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')
        filtered = self.get_queryset().filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(applicant_requirements__icontains=q) |
            Q(position__title__icontains=q) |
            Q(position__skills__name__icontains=q)
        )
        context['searchform'] = SearchBarForm(initial={'q': q})
        context['filtered'] = filtered
        return context


class ApplicationsList(CustomLoginRequired, ListView):
    """View that displays all applications to the user's projects and
    any applications from the user to other user's projects
    """
    model = Application

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset = queryset.filter(
            Q(position__project__owner=self.request.user) |
            Q(user=self.request.user)
        ).select_related(
            'position', 'user'
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
                filtered = filtered.filter(
                    position__project__slug=q
                )
            elif category == 'need':
                filtered = filtered.filter(
                    position__slug=q
                )
        context['searchform'] = SearchBarForm()
        context['q'] = self.kwargs['q']
        context['box'] = self.kwargs['box']
        context['filtered'] = filtered
        context['inbox_count'] = self.get_queryset().filter(
            status='U',
            position__project__owner=self.request.user
        ).count()
        return context


class UpdateAppStatus(CustomLoginRequired, View):
    """View that handles JSON requests for changing the status of an
    application
    """
    http_method_names = ['post', ]

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


class CreateApp(CustomLoginRequired, View):
    """View for creating an application instance - if the user applies
    to an open position
    """
    http_method_names = ['post', ]

    def post(self, request, *args, **kwargs):
        position_pk = self.request.POST.get('position_pk')
        position = Position.objects.get(id=position_pk)
        user = self.request.user
        try:
            app = Application(
                user=user,
                position=position,
                status='U'
            )
            app.save()
            data = {
                'updated': True,
            }
            return JsonResponse(data)

        except Exception as err:
            data = {
                'updated': False,
            }
            return JsonResponse(data)


class ProjectView(CustomLoginRequired, PrefetchRelatedMixin, DetailView):
    """View for displaying the details of a specific project
    """
    model = Project
    template_name = 'projects/project.html'
    prefetch_related = ['position_set', 'position_set__skills', ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['searchform'] = SearchBarForm()
        return context


@login_required
def create_update_project(request, slug=None):
    """View for handling the editing of a specific project and its
    related positions
    """
    request_user = request.user
    if slug is not None:
        project = Project.objects.get(slug=slug)
        project_form = CreateProjectForm(instance=project)
        position_formset = PositionFormset(
            queryset=Position.objects.filter(
                project=project
            ))
    else:
        project = None
        project_form = CreateProjectForm()
        position_formset = PositionFormset(
            queryset=Position.objects.none()
        )

    if request.method == 'POST':
        project_form = CreateProjectForm(
            request.POST, 
            instance=project
        )
        position_formset = PositionFormset(
            request.POST,
            queryset=Position.objects.filter(project=project)
        )
        if project_form.is_valid() and position_formset.is_valid():
            project = project_form.save(commit=False)
            project.owner = request_user
            new_project = False
            if project.status is None:
                new_project = True
                project.status = 'A'
            project.save()
            positions = position_formset.save(commit=False)
            for position in positions:
                position.project = project
                if position.status not in ('E', 'F'):
                    position.status = 'E'
                position.save()
            position_formset.save_m2m()
            position_formset.save()
            if new_project:
                messages.success(
                    request, 'Project {} created!'.format(project.title))
            else:
                messages.success(
                    request, 'Project {} updated!'.format(project.title))
            return HttpResponseRedirect(reverse('projects:project', kwargs={'slug': project.slug}))

    context = {
        'project_form': project_form,
        'position_formset': position_formset,
    }
    return render(request, 'projects/create_update_project.html', context)


class DeleteProject(DeleteView):
    """Handles the deletion of a specific project
    """
    model = Project
    success_url = reverse_lazy('projects:dashboard', kwargs={'category':'all', 'q':'all'})
