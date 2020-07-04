import debug_toolbar

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from markdownx import urls as markdownx

from .views import RootRedirect

urlpatterns = [
    path('', RootRedirect.as_view()),
    path('adminymin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('projects/', include('projects.urls', namespace='projects')),
    path('select2/', include('django_select2.urls')),
    # path('__debug__/', include(debug_toolbar.urls)),
    path('markdownx/', include(markdownx)),
]

if settings.Debug:
    urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
