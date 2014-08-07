import sys

sys.path.append('../..')

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from social.apps.tornado_app.models import init_social
from social.apps.tornado_app.routes import SOCIAL_AUTH_ROUTES

import settings


engine = create_engine('sqlite:///test.db', echo=False)
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/home.html')


class DoneHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        from models import User
        user_id = self.get_secure_cookie('user_id')
        user = session.query(User).get(int(user_id))
        self.render('templates/done.html', user=user)


class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.request.redirect('/')


tornado.options.parse_command_line()
tornado_settings = dict((k, getattr(settings, k)) for k in dir(settings)
                        if not k.startswith('__'))
application = tornado.web.Application(SOCIAL_AUTH_ROUTES + [
    (r'/', MainHandler),
    (r'/done/', DoneHandler),
    (r'/logout/', LogoutHandler),
], cookie_secret='adb528da-20bb-4386-8eaf-09f041b569e0',
   **tornado_settings)


def main():
    init_social(Base, session, tornado_settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()


def syncdb():
    from models import user_syncdb
    init_social(Base, session, tornado_settings)
    Base.metadata.create_all(engine)
    user_syncdb()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'syncdb':
        syncdb()
    else:
        main()
