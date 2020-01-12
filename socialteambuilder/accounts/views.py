# accounts/views.py

from braces.views import PrefetchRelatedMixin

from django.contrib import messages
from django.contrib.auth import get_user_model
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
    View
)
from django.urls import reverse_lazy

from django.contrib.auth.forms import AuthenticationForm

from .forms import (
    UserCreationForm, 
    UserUpdateForm, 
    NewPortfolioProjectFormset
)
from .models import PortfolioProject, Skill
from projects.models import Application

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


def update_user(request, pk): # do we need pk here?
    user = request.user
    # user_skills = Skill.objects.filter(
    #     users__id=user.id
    # ).values()
    # user_data = {
    #     'first_name':  user.first_name,
    #     'last_name': user.last_name,
    #     'about': user.about,
    #     'avatar': user.avatar,
    #     'skills': Skill.objects.filter(users=user)
    # } 
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
    applications = Application.objects.filter(
        user=user
    ).prefetch_related(
        'position__skills',
    ).select_related(
        'position__project'
    )

    
    if request.method == 'POST':
        user_form = UserUpdateForm(data=request.POST, instance=user)
        project_formset = NewPortfolioProjectFormset(
            request.POST,
            queryset=PortfolioProject.objects.filter(user=user)
        )
        print("request data: ", request.POST)
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
            return HttpResponse("working")

    context = {
        'user_form': user_form,
        'project_formset': project_formset,
        'applications': applications
    }
    return render(request, 'accounts/profile.html', context)
