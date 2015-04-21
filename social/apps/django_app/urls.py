"""URLs module"""
from django.conf import settings
try:
    from django.conf.urls import patterns, url
except ImportError:
    # Django < 1.4
    from django.conf.urls.defaults import patterns, url


from social.utils import setting_name


extra = getattr(settings, setting_name('TRAILING_SLASH'), True) and '/' or ''


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
