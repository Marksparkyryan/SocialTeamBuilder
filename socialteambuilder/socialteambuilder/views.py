from django.views.generic import RedirectView

from django.http import HttpResponseRedirect, HttpResponseGone
from django.urls import reverse_lazy
from django.shortcuts import HttpResponsePermanentRedirect


class RootRedirect(RedirectView):
    """A redirect view to register for the root of the website
    """
    url = reverse_lazy('accounts:register')

    def get(self, request, *args, **kwargs):
        super().__get__(request, *args, **kwargs)
        if request.user.is_authenticated:
            url = reverse_lazy('projects:dashboard', kwargs={
                'category': 'all',
                'q': 'all'
            }) 
        else:
            url = self.get_redirect_url(*args, **kwargs)
        if url:
            if self.permanent:
                return HttpResponsePermanentRedirect(url)
            else:
                return HttpResponseRedirect(url)
        else:
            logger.warning(
                'Gone: %s', request.path,
                extra={'status_code': 410, 'request': request}
            )
            return HttpResponseGone()

