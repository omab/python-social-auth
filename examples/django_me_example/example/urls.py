from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin


PATH = getattr(settings, 'URL_PATH', '')

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup-email/', 'example.app.views.signup_email'),
    url(r'^email-sent/', 'example.app.views.validation_sent'),
    url(r'^%s$' % PATH, 'example.app.views.home'),
    url(r'^%sdone/$' % PATH, 'example.app.views.done', name='done'),
    url(r'^%semail/$' % PATH, 'example.app.views.require_email',
        name='require_email'),
    url(r'%s' % PATH, include('social.apps.django_app.urls',
        namespace='social'))
)
