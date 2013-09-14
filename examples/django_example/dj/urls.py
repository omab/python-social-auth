from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin


PATH = getattr(settings, 'URL_PATH', '')

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^%s$' % PATH, 'example.views.home'),
    url(r'^%sdone/$' % PATH, 'example.views.done', name='done'),
    url(r'^%semail/$' % PATH, 'example.views.require_email',
        name='require_email'),
    url(r'%s' % PATH, include('social.apps.django_app.urls',
        namespace='social'))
)
