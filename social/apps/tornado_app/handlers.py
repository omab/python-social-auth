import tornado.web

from social.apps.tornado_app.utils import strategy
from social.actions import do_auth, do_complete, do_disconnect


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.strategy.get_user(
            self.get_secure_cookie("user_id")
        )

    def login_user(self, user):
        self.set_secure_cookie("user_id", user.id)


class AuthHandler(tornado.web.RequestHandler):
    def get(self, backend):
        self._auth(backend)

    def post(self, backend):
        self._auth(backend)

    @strategy("complete")
    def _auth(self, backend):
        do_auth(self.strategy)


class CompleteHandler(tornado.web.RequestHandler):
    def get(self, backend):
        self._complete(backend)

    def post(self, backend):
        self._complete(backend)

    @strategy("complete")
    def _complete(self, backend):
        do_complete(self.strategy,
                    login=lambda strategy, user: self.login_user(user),
                    user=self.get_current_user())


class DisconnectHandler(tornado.web.RequestHandler):
    def post(self):
        do_disconnect()
