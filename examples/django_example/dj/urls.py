from django.conf import settings
from django.conf.urls import patterns, include, url


PATH = getattr(settings, 'URL_PATH', '')

urlpatterns = patterns('',
    url(r'^%s$' % PATH, 'example.views.home'),
    url(r'^%sdone/$' % PATH, 'example.views.done', name='done'),
    url(r'%s' % PATH, include('social.apps.django_app.urls',
        namespace='social'))
)
