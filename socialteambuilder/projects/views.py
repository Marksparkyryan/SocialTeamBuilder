# projects/views

from braces.views import PrefetchRelatedMixin

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.db.models import Q
from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    HttpResponseRedirect,
    Http404
)
from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, DeleteView, CreateView
from django.views.generic.detail import SingleObjectMixin
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
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        """get distinct projects that are currently open and have empty
        positions
        """
        super().get_queryset(*args, **kwargs)
        queryset = self.queryset.filter(
            status='A',
            position__status='E'
        ).distinct()
        category = self.kwargs['category']
        q = self.kwargs['q']
        if q != 'all':
            if category == 'need':
                queryset = queryset.filter(
                    position__slug=q
                )
            elif category == 'skill':
                queryset = queryset.filter(
                    position__skills__name=q
                )
            elif category == 'skills':
                not_user_positions = Position.objects.exclude(
                    applications__user=self.request.user
                )
                queryset = queryset.filter(
                    Q(position__skills__in=self.request.user.skills.all()) &
                    Q(position__in=[position for position in not_user_positions])
                )
            elif category == 'my-opps':
                not_user_positions = Position.objects.exclude(
                    applications__user=self.request.user
                )
                queryset = queryset.filter(
                    position__in=[position for position in not_user_positions]
                )
            elif category == 'accepted':
                queryset = queryset.filter(
                    Q(position__applications__user=self.request.user) &
                    Q(position__applications__status='R')
                )
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['searchform'] = SearchBarForm()
        context['q'] = self.kwargs['q']
        return context


class SearchBar(CustomLoginRequired, ListView):
    """View that handles queries submitted by the SearchForm
    """
    queryset = Project.objects.all()
    template_name = 'projects/dashboard.html'
    paginate_by = 5

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if request.GET.get('q') is not None:
            request.session['q'] = request.GET.get('q')
        self.q = request.session['q']
        print(self.q)

    def get_queryset(self, *args, **kwargs):
        """get distinct projects that are currently open and have empty
        positions
        """
        super().get_queryset(*args, **kwargs)
        queryset = self.queryset.filter(
            status='A',
            position__status='E'
        ).distinct()
        q = self.q
        queryset = queryset.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(applicant_requirements__icontains=q) |
            Q(position__title__icontains=q) |
            Q(position__skills__name__icontains=q)
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['searchform'] = SearchBarForm(initial={'q': self.q})
        context['query'] = self.q
        return context


class ApplicationsList(CustomLoginRequired, ListView):
    """View that displays all applications to the user's projects and
    any applications from the user to other user's projects
    """
    model = Application
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            Q(position__project__owner=self.request.user) |
            Q(user=self.request.user)
        ).select_related(
            'position', 'user'
        ).distinct()
        box = self.kwargs['box']
        if box == 'inbox':
            queryset = queryset.filter(
                position__project__owner=self.request.user
            )
        elif box == 'outbox':
            queryset = queryset.filter(
                user=self.request.user
            )
        category = self.kwargs['category']
        q = self.kwargs['q']
        if q != 'all':
            if category == 'status':
                queryset = queryset.filter(
                    status__icontains=q
                )
            elif category == 'project':
                queryset = queryset.filter(
                    position__project__slug=q
                )
            elif category == 'need':
                queryset = queryset.filter(
                    position__slug=q
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context['searchform'] = SearchBarForm()
        context['q'] = self.kwargs['q']
        context['box'] = self.kwargs['box']
        context['inbox_count'] = self.get_queryset().filter(
            status='U',
            position__project__owner=self.request.user
        ).count()
        return context


class UpdateAppStatus(CustomLoginRequired, SingleObjectMixin, View):
    """View that handles ajax requests for changing the status of an
    application
    """
    model = Application
    http_method_names = ['post']

    def render_json_response(self, message, success):
        return JsonResponse({
            "message": message,
            "success": success
        })

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.kwargs.update({"pk": request.POST.get('app_pk')})

    def get_object(self):
        application = super().get_object()
        if application.position.project.owner != self.request.user:
            raise PermissionDenied
        return application

    def position_is_filled(self):
        app = self.get_object()
        return app.position.status == 'F'

    def update_app_status(self, status, unread):
        app = self.get_object()
        app.status = status
        app.unread = unread
        app.save()

    def update_outstanding_apps(self):
        app = self.get_object()
        outstanding = Application.objects.filter(
                position=app.position,
                status='U'
            )
        for app in outstanding:
            app.status = 'R'
            app.unread = True
            app.save()

    def post(self, request, *args, **kwargs):
        if self.position_is_filled():
            return self.render_json_response("Position is filled", False)
        status = self.request.POST.get('status')
        user = self.request.user
        app = self.get_object()
        position = app.position
        if status == 'A':
            self.update_app_status(status, True)
            position.status = 'F'
            position.save()
            self.update_outstanding_apps()
            # get refreshed app from db
            app = self.get_object()
            return self.render_json_response(app.get_status_display(), True)
        elif status == 'R':
            self.update_app_status(status, True)
            return self.render_json_response(app.get_status_display(), True)
        return self.render_json_response("Invalid or missing status", False)


class CreateApp(CustomLoginRequired, View):
    """View for handling ajax requests to create applications for requesting
    user and returning a jsonResponse
    """
    http_method_names = ['post']
    model = Application

    def render_json_response(self, message, success, status):
        return JsonResponse({
            "message": message,
            "success": success
        }, status=status)

    def post(self, request, *args, **kwargs):
        position = get_object_or_404(
            Position, 
            pk=request.POST.get('position_pk')
        )
        try:
            app = self.model.objects.get(
                user=request.user,
                position=position
                )
            return self.render_json_response(
                "Application already exists for this position and user", 
                False,
                400 
            )
        except self.model.DoesNotExist:
            app = self.model(
                user=request.user,
                position=position,
                status='U'
            )
            app.save()
            return self.render_json_response(str(app), True, 201)


class ProjectView(CustomLoginRequired, PrefetchRelatedMixin, DetailView):
    """View for displaying the details of a specific project
    """
    model = Project
    template_name = 'projects/project.html'
    prefetch_related = ['position_set', 'position_set__skills']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['searchform'] = SearchBarForm()
        completed = Application.objects.filter(
            position__project=self.get_object(),
            status='A'
        )
        context['completed'] = completed
        return context


@login_required
def create_update_project(request, slug=None):
    """View for handling the editing of a specific project and its
    related positions
    """
    request_user = request.user
    if slug is not None:
        project = Project.objects.get(slug=slug)
        if project.owner != request.user:
            raise PermissionDenied
        else:
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
    queryset = Project.objects.all()
    success_url = reverse_lazy('projects:dashboard', kwargs={'category':'all', 'q':'all'})

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if project.owner != request.user:
            raise PermissionDenied
        super().dispatch(self, request, *args, **kwargs)


