import sys

sys.path.append('../..')

from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from sqlalchemy import engine_from_config

from social.apps.pyramid_app.models import init_social

from .models import DBSession, Base


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    session_factory = UnencryptedCookieSessionFactoryConfig('thisisasecret')
    config = Configurator(settings=settings,
                          session_factory=session_factory,
                          autocommit=True)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_request_method('example.auth.get_user', 'user', reify=True)
    config.add_route('home', '/')
    config.add_route('done', '/done')
    config.include('example.settings')
    config.include('example.local_settings')
    config.include('social.apps.pyramid_app')
    init_social(config, Base, DBSession)
    config.scan()
    config.scan('social.apps.pyramid_app')
    return config.make_wsgi_app()
