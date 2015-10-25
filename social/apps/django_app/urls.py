"""URLs module"""
from django import VERSION
from django.conf import settings
from django.conf.urls import url
from social.apps.django_app import views

from social.utils import setting_name


extra = getattr(settings, setting_name('TRAILING_SLASH'), True) and '/' or ''

urlpatterns = (
    # authentication / association
    url(r'^login/(?P<backend>[^/]+){0}$'.format(extra),
        views.auth,
        name='begin'),
    url(r'^complete/(?P<backend>[^/]+){0}$'.format(extra),
        views.complete,
        name='complete'),
    # disconnection
    url(r'^disconnect/(?P<backend>[^/]+){0}$'.format(extra),
        views.disconnect,
        name='disconnect'),
    url(r'^disconnect/(?P<backend>[^/]+)/(?P<association_id>[^/]+){0}$'
            .format(extra),
        views.disconnect,
        name='disconnect_individual'),
)
