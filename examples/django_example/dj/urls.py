from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'example.views.home'),
    url(r'^done/$', 'example.views.done'),
    url('', include('social.apps.django_app.urls', namespace='social'))
)
