# accounts/views.py

from braces.views import PrefetchRelatedMixin

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import (
    RedirectView,
    TemplateView,
    CreateView,
    UpdateView,
    View,
    DetailView
)
from django.urls import reverse_lazy, reverse

from .forms import (
    UserCreationForm, 
    UserUpdateForm, 
    NewPortfolioProjectFormset
    
)
from .models import PortfolioProject, Skill
from projects.models import Application
from projects.views import CustomLoginRequired

User = get_user_model()


class Register(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('projects:dashboard')
    template_name = 'accounts/register.html' 


class Activate(UserPassesTestMixin, RedirectView):
    """View handling the verification of the emailed token and setting
    of user to active status so they can log in. If token is not valid,
    a 403 forbidden.
    """
    url = reverse_lazy("auth:login")

    def test_func(self):
        """If the token is valid, return True, else return False
        """
        user = User.objects.get(id=self.kwargs['pk'])
        token = self.kwargs['token']
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return True
        return False


class LogIn(LoginView):
    def form_valid(self, form): 
        response = super().form_valid(form)
        messages.add_message(self.request, "You're logged in!") # this is not working
        return response


@login_required()
def update_user(request):
    user = request.user
    instance = User.objects.filter(
        id=user.id
    ).prefetch_related(
        'skills',
        'portfolio_projects',
    ).first()
    user_form = UserUpdateForm(instance=instance)
    project_formset = NewPortfolioProjectFormset(
        queryset=PortfolioProject.objects.filter(user=user)
    )
    # get user's accepted applications from completed projects
    applications = Application.objects.filter(
        user=user,
        status='A',
        position__project__status='C'
    ).prefetch_related(
        'position__skills',
    ).select_related(
        'position__project'
    )

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        project_formset = NewPortfolioProjectFormset(
            request.POST,
            queryset=PortfolioProject.objects.filter(user=user)
        )
        print("request data: ", request.POST)
        print(request.FILES)
        if user_form.is_valid() and project_formset.is_valid():
            # user info form
            user_form.save()
            # portfolio project forms
            projects = project_formset.save(commit=False)
            # print(dir(project_formset))
            for project in project_formset.data:
                print(project)
            for project in project_formset.deleted_forms:
                print(project)
            for project in project_formset.deleted_objects:
                print("deleting", project)
                project.delete()
            for project in projects:
                project.user_id = user.id
                project.save()

            messages.success(request, 'Profile updated successfully!')
            return HttpResponseRedirect(reverse('accounts:profile'))

    context = {
        'user_form': user_form,
        'project_formset': project_formset,
        'applications': applications
    }
    return render(request, 'accounts/edit_profile.html', context)


class Profile(CustomLoginRequired, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = User.objects.filter(
            id=self.request.user.id
            ).prefetch_related(
                'skills',
                'portfolio_projects',
            ).first()
        # get user's accepted applications from completed projects
        context['applications'] = Application.objects.filter(
            user=self.request.user,
            status='A',
            position__project__status='C'
        )
        return context






    
