"""URLs module"""
from django import VERSION
from django.conf import settings
from social.utils import setting_name


extra = getattr(settings, setting_name('TRAILING_SLASH'), True) and '/' or ''

if VERSION >= (1, 8):
    from django.conf.urls import url
    from social.apps.django_app import views

    urlpatterns = [
        # authentication / association
        url(r'^login/(?P<backend>[^/]+){0}$'.format(extra), views.auth,
            name='begin'),
        url(r'^complete/(?P<backend>[^/]+){0}$'.format(extra), views.complete,
            name='complete'),
        # disconnection
        url(r'^disconnect/(?P<backend>[^/]+){0}$'.format(extra), views.disconnect,
            name='disconnect'),
        url(r'^disconnect/(?P<backend>[^/]+)/(?P<association_id>[^/]+){0}$'
            .format(extra), views.disconnect, name='disconnect_individual'),
    ]
else:  # Django < 1.8, deprecated code, remove it after Django 1.9 release (in December 2015)

    try:
        from django.conf.urls import patterns, url
    except ImportError:
        # Django < 1.4
        from django.conf.urls.defaults import patterns, url

    urlpatterns = patterns('social.apps.django_app.views',
                           # authentication / association
                           url(r'^login/(?P<backend>[^/]+){0}$'.format(extra), 'auth',
                               name='begin'),
                           url(r'^complete/(?P<backend>[^/]+){0}$'.format(extra), 'complete',
                               name='complete'),
                           # disconnection
                           url(r'^disconnect/(?P<backend>[^/]+){0}$'.format(extra), 'disconnect',
                               name='disconnect'),
                           url(r'^disconnect/(?P<backend>[^/]+)/(?P<association_id>[^/]+){0}$'
                               .format(extra), 'disconnect', name='disconnect_individual'),
                           )
