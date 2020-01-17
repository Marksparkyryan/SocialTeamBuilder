# accounts/views.py

from braces.views import PrefetchRelatedMixin

from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import (
    RedirectView,
    TemplateView,
    CreateView,
    UpdateView,
    View,
    DetailView
)
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode

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
    success_url = reverse_lazy('accounts:check_inbox')
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        to_email = form.cleaned_data.get('email')
        subject = 'Activate Your Social Team Builder Account'
        token = default_token_generator.make_token(user)
        pre_check = default_token_generator.check_token(user, token)
        print("pre-check token: ", pre_check)
        print("token sent: ", token)
        print("to user: ", user)
        message = render_to_string('accounts/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
        })
        email = EmailMessage(
                        subject, message, to=[to_email]
            )
        email.send()
        return super().form_valid(form) 


class CheckInbox(TemplateView):
    template_name = "accounts/check_inbox.html"


class Activate(UserPassesTestMixin, RedirectView):
    """View handling the verification of the emailed token and setting
    of user to active status so they can log in. If token is not valid,
    a 403 forbidden.
    """
    url = reverse_lazy("accounts:dashboard")

    def test_func(self):
        """If the token is valid, return True, else return False
        """
        uid = force_text(urlsafe_base64_decode(self.kwargs.get('uidb64')))
        user = User.objects.get(pk=uid)
        
        token = self.kwargs['token']
        print("token received: ", token)
        print("for user: ", user)
        print("token checker: ", default_token_generator.check_token(user, token))
        if default_token_generator.check_token(user, token):
            user.is_active = True
            print("user activated by token")
            user.save()
            return True
        print("token activation failed")
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
        # print("request data: ", request.POST)
        print(project_formset)
        if user_form.is_valid() and project_formset.is_valid():
            # user info form
            user_form.save()
            # portfolio project forms
            projects = project_formset.save(commit=False)
            for project in project_formset.deleted_objects:
                project.delete()
            for project in projects:
                project.user_id = user.id
                project.save()
            # print(project_formset.cleaned_data)
            # print(project_formset.data)
            project_formset.save_m2m()
            messages.success(request, 'Profile updated successfully!')
            return HttpResponseRedirect(reverse('accounts:profile', kwargs={'pk': user.pk}))

    context = {
        'user_form': user_form,
        'project_formset': project_formset,
        'applications': applications
    }
    return render(request, 'accounts/edit_profile.html', context)


class Profile(CustomLoginRequired, DetailView):
    model = User
    template_name = "accounts/profile.html"
    context_object_name = "user_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get user's accepted applications from completed projects
        context['applications'] = Application.objects.filter(
            user=self.request.user,
            status='A',
            position__project__status='C'
        )
        return context






    
