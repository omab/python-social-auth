from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'example.app.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup-email/', 'example.app.views.signup_email'),
    url(r'^email-sent/', 'example.app.views.validation_sent'),
    url(r'^login/$', 'example.app.views.home'),
    url(r'^logout/$', 'example.app.views.logout'),
    url(r'^done/$', 'example.app.views.done', name='done'),
    url(r'^email/$', 'example.app.views.require_email', name='require_email'),
    url(r'', include('social.apps.django_app.urls', namespace='social'))
)
