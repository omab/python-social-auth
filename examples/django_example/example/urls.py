from django.conf.urls import patterns, include, url
from django.contrib import admin
from social.apps.django_app.views import complete as social_complete_view
from django.views.decorators.csrf import csrf_exempt


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', social_complete_view, kwargs=dict(backend='azuread-b2c')),
    url(r'^home$', 'example.app.views.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^email-sent/', 'example.app.views.validation_sent'),
    url(r'^login/$', 'example.app.views.home'),
    url(r'^logout/$', 'example.app.views.logout'),
    url(r'^done/$', 'example.app.views.done', name='done'),
    url(r'^ajax-auth/(?P<backend>[^/]+)/$', 'example.app.views.ajax_auth',
        name='ajax-auth'),
    url(r'^email/$', 'example.app.views.require_email', name='require_email'),
    url(r'', include('social.apps.django_app.urls', namespace='social'))
)
