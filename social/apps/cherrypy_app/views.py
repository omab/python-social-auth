import cherrypy

from social.utils import setting_name, module_member
from social.actions import do_auth, do_complete, do_disconnect
from social.apps.cherrypy_app.utils import strategy


class CherryPyPSAViews(object):
    @cherrypy.expose
    @strategy('/complete/%(backend)s')
    def login(self, backend):
        return do_auth(self.strategy)

    @cherrypy.expose
    @strategy('/complete/%(backend)s')
    def complete(self, backend, *args, **kwargs):
        login = cherrypy.config.get(setting_name('LOGIN_METHOD'))
        do_login = module_member(login) if login else self.do_login
        user = getattr(cherrypy.request, 'user', None)
        return do_complete(self.strategy, do_login, user=user, *args, **kwargs)

    @cherrypy.expose
    def disconnect(self, backend, association_id=None):
        user = getattr(cherrypy.request, 'user', None)
        return do_disconnect(self.strategy, user, association_id)

    def do_login(self, strategy, user):
        strategy.session_set('user_id', user.id)
