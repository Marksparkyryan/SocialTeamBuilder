from django.urls import reverse_lazy
from django.views.generic import RedirectView


class RootRedirect(RedirectView):
    """A redirect view to register for the root of the website
    """
    url = reverse_lazy('accounts:register')
