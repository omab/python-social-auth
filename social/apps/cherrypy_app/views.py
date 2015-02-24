import cherrypy

from social.utils import setting_name, module_member
from social.actions import do_auth, do_complete, do_disconnect
from social.apps.cherrypy_app.utils import psa


class CherryPyPSAViews(object):
    @cherrypy.expose
    @psa('/complete/%(backend)s')
    def login(self, backend):
        return do_auth(self.backend)

    @cherrypy.expose
    @psa('/complete/%(backend)s')
    def complete(self, backend, *args, **kwargs):
        login = cherrypy.config.get(setting_name('LOGIN_METHOD'))
        do_login = module_member(login) if login else self.do_login
        user = getattr(cherrypy.request, 'user', None)
        return do_complete(self.backend, do_login, user=user, *args, **kwargs)

    @cherrypy.expose
    @psa()
    def disconnect(self, backend, association_id=None):
        user = getattr(cherrypy.request, 'user', None)
        return do_disconnect(self.backend, user, association_id)

    def do_login(self, backend, user, social_user):
        backend.strategy.session_set('user_id', user.id)
