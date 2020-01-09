from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.tokens import default_token_generator
from django.views.generic import RedirectView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.forms import AuthenticationForm 


User = get_user_model()


class Activate(UserPassesTestMixin, RedirectView):
    """View handling the verification of the emailed token and setting
    of user to active status so they can log in. If token is not valid,
    a 403 forbidden.
    """
    url = reverse_lazy("accounts:login")

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


class LogIn(FormView):
    form_class = AuthenticationForm
    # success_url = reverse_lazy("posts:all")
    template_name = "accounts/login.html"
    
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())
    
    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)
    pass

