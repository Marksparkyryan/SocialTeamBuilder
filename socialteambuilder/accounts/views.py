# accounts/views.py

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.views.generic import RedirectView, TemplateView, CreateView
from django.urls import reverse_lazy

from django.contrib.auth.forms import AuthenticationForm

from .forms import UserCreationForm


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


