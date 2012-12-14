"""URLs module"""
from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('social.apps.dj.views',
    # authentication / association
    url(r'^login/(?P<backend>[^/]+)/$', 'auth',
        name='socialauth_begin'),
    url(r'^complete/(?P<backend>[^/]+)/$', 'complete',
        name='socialauth_complete'),
    # disconnection
    url(r'^disconnect/(?P<backend>[^/]+)/$', 'disconnect',
        name='socialauth_disconnect'),
    url(r'^disconnect/(?P<backend>[^/]+)/(?P<association_id>\d+)/$',
        'disconnect', name='socialauth_disconnect_individual'),
)
