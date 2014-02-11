import sys

sys.path.append('../..')

import cherrypy

from jinja2 import Environment, FileSystemLoader

from social.apps.cherrypy_app.utils import backends
from social.apps.cherrypy_app.views import CherryPyPSAViews

from db.saplugin import SAEnginePlugin
from db.satool import SATool
from db.user import User


SAEnginePlugin(cherrypy.engine, 'sqlite:///test.db').subscribe()


class PSAExample(CherryPyPSAViews):
    @cherrypy.expose
    def index(self):
        return self.render_to('home.html')

    @cherrypy.expose
    def done(self):
        user = getattr(cherrypy.request, 'user', None)
        if user is None:
            raise cherrypy.HTTPRedirect('/')
        return self.render_to('done.html', user=user, backends=backends(user))

    @cherrypy.expose
    def logout(self):
        raise cherrypy.HTTPRedirect('/')

    def render_to(self, tpl, **ctx):
        return cherrypy.tools.jinja2env.get_template(tpl).render(**ctx)


def load_user():
    user_id = cherrypy.session.get('user_id')
    if user_id:
        cherrypy.request.user = cherrypy.request.db.query(User).get(user_id)
    else:
        cherrypy.request.user = None


def session_commit():
    cherrypy.session.save()


try:
    from local_settings import SOCIAL_SETTINGS
except ImportError:
    print 'Define a local_settings.py using local_settings.py.template as base'
    SOCIAL_SETTINGS = {}


if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_port': 8000,
        'tools.sessions.on': True,
        'tools.sessions.storage_type': 'ram',
        'tools.db.on': True,
        'tools.authenticate.on': True,
        'SOCIAL_AUTH_USER_MODEL': 'db.user.User',
        'SOCIAL_AUTH_LOGIN_URL': '/',
        'SOCIAL_AUTH_LOGIN_REDIRECT_URL': '/done',
    })
    cherrypy.config.update(SOCIAL_SETTINGS)
    cherrypy.tools.jinja2env = Environment(
        loader=FileSystemLoader('templates')
    )
    cherrypy.tools.db = SATool()
    cherrypy.tools.authenticate = cherrypy.Tool('before_handler', load_user)
    cherrypy.tools.session = cherrypy.Tool('on_end_resource', session_commit)
    cherrypy.quickstart(PSAExample())
