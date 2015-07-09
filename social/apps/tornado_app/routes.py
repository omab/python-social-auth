from tornado.web import url

from .handlers import AuthHandler, CompleteHandler, DisconnectHandler


SOCIAL_AUTH_ROUTES = [
    url(r'/login/(?P<backend>[^/]+)/?', AuthHandler, name='begin'),
    url(r'/complete/(?P<backend>[^/]+)/?', CompleteHandler, name='complete'),
    url(r'/disconnect/(?P<backend>[^/]+)/?', DisconnectHandler,
        name='disconnect'),
    url(r'/disconnect/(?P<backend>[^/]+)/(?P<association_id>\d+)/?',
        DisconnectHandler, name='disconect_individual'),
]
