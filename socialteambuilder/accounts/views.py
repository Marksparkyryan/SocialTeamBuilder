# accounts/views.py
from django.utils import timezone

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import (
    TemplateView,
    CreateView,
    DetailView
)
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode

from projects.forms import SearchBarForm
from projects.models import Application
from projects.views import CustomLoginRequired

from .forms import (
    MyAuthenticationForm,
    UserCreationForm,
    UserUpdateForm,
    NewPortfolioProjectFormset,
    AvatarForm
)
from .models import PortfolioProject

User = get_user_model()


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """Custom token generator for users to use for one-time account
    activation
    """

    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) + str(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()


class Register(SuccessMessageMixin, CreateView):
    """View for registering users. Confirmation email and token is 
    delivered from this view.
    """
    form_class = UserCreationForm
    success_url = reverse_lazy('projects:dashboard', kwargs= {'q': 'all', 'category': 'all'})
    success_message = "You're registered!"
    template_name = 'accounts/register.html'


    def form_valid(self, form):
        if settings.USE_TOKEN_AUTH_WITH_DUMMY_INBOX:
            user = form.save(commit=False)
            user.is_active = False
            user.last_login = timezone.now()
            user.save()
            current_site = get_current_site(self.request)
            to_email = form.cleaned_data.get('email')
            subject = 'Activate Your Social Team Builder Account'
            token = account_activation_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            email = EmailMessage(
                subject, message, to=[to_email]
            )
            email.send()
            success_message = "Check your inbox!"
            self.success_url = reverse_lazy('accounts:check_inbox', kwargs={
            'token': token
            })

        else:
            user = form.save(commit=False)
            user.is_active = True
            user.save()

        return super().form_valid(form)


class CheckInbox(TemplateView):
    """View for registration success message
    """
    template_name = "accounts/check_inbox.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['domain'] = get_current_site(self.request)
        context['uid'] = urlsafe_base64_encode(force_bytes(self.request.user.pk))
        context['token'] = kwargs['token']
        return context

def activate(request, uidb64, token):
    """View for handling the verification of token kwarg. If valid, the
    user's active status is set to True
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(
            request, "Your account has been confirmed and activated!")
        return HttpResponseRedirect(reverse('accounts:updateuser'))
    else:
        return render(request, 'accounts/failed_activation.html')


class LogIn(SuccessMessageMixin, LoginView):
    """View for handling logging in of user
    """
    form_class = MyAuthenticationForm
    
    def get_success_message(self, cleaned_data):
        super().get_success_message(cleaned_data)
        return 'Welcome back, {}!'.format(self.request.user.first_name)

    def get_current_user(self):
        return self.request.user.first_name


@login_required()
def update_user(request):
    """View for handling the editing of a user instance
    """
    user = request.user
    instance = User.objects.get(id=user.id)
    avatar_form = AvatarForm(instance=instance)
    user_form = UserUpdateForm(instance=instance)
    project_formset = NewPortfolioProjectFormset(
        queryset=PortfolioProject.objects.filter(user=user)
    )
    # get user's accepted applications from completed projects
    applications = Application.objects.filter(
        user=user,
        status='A',
        position__project__status='C'
    ).select_related(
        'position__project'
    )

    if request.method == 'POST':
        if request.is_ajax():
            avatar_form = AvatarForm(request.POST, request.FILES, instance=instance)
            if avatar_form.is_valid():
                user.avatar = request.FILES['id_avatar']
                print("avatar_form is valid and saving: ", user.avatar)
                user.save()
                return HttpResponse(status=200)
            return HttpResponse(status=400)
        else:
            user_form = UserUpdateForm(request.POST, request.FILES, instance=user)
            project_formset = NewPortfolioProjectFormset(
                request.POST,
                queryset=PortfolioProject.objects.filter(user=user)
            )
            print('----------------')
            print(project_formset.data)
            if user_form.is_valid() and project_formset.is_valid():
                user_form.save() 
                projects = project_formset.save(commit=False)
                for project in projects:
                    project.user = user
                    project.save()
                project_formset.save()

                messages.success(request, 'Profile updated successfully!')
                return HttpResponseRedirect(reverse('accounts:profile', kwargs={'pk': user.pk}))
        

    context = {
        'searchform': SearchBarForm(),
        'user_form': user_form,
        'project_formset': project_formset,
        'applications': applications,
        'avatar_form': avatar_form
    }
    return render(request, 'accounts/edit_profile.html', context)


class Profile(CustomLoginRequired, DetailView):
    """View for the detail of user's information
    """
    model = User
    template_name = "accounts/profile.html"
    context_object_name = "user_profile"
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['searchform'] = SearchBarForm()
        # get user's accepted applications from completed projects
        context['applications'] = Application.objects.filter(
            user=self.request.user,
            status='A',
            position__project__status='C'
        )
        return context
