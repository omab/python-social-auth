import json

from tornado.template import Loader, Template

from social.utils import build_absolute_uri
from social.strategies.base import BaseStrategy, BaseTemplateStrategy


class TornadoTemplateStrategy(BaseTemplateStrategy):
    def render_template(self, tpl, context):
        path, tpl = tpl.rsplit('/', 1)
        return Loader(path).load(tpl).generate(**context)

    def render_string(self, html, context):
        return Template(html).generate(**context)


class TornadoStrategy(BaseStrategy):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('tpl', TornadoTemplateStrategy)
        self.request_handler = kwargs.get('request_handler')
        super(TornadoStrategy, self).__init__(*args, **kwargs)

    def get_setting(self, name):
        return self.request_handler.settings[name]

    def request_data(self, merge=True):
        return self.request.arguments.copy()

    def request_host(self):
        return self.request.host

    def redirect(self, url):
        return self.request_handler.redirect(url)

    def html(self, content):
        self.request_handler.write(content)

    def session_get(self, name, default=None):
        return self.request_handler.get_secure_cookie(name, value=default)

    def session_set(self, name, value):
        self.request_handler.set_secure_cookie(name, str(value))

    def session_pop(self, name):
        value = self.request_handler.get_secure_cookie(name)
        self.request_handler.set_secure_cookie(name, '')
        return value

    def session_setdefault(self, name, value):
        pass

    def build_absolute_uri(self, path=None):
        return build_absolute_uri('{0}://{1}'.format(self.request.protocol,
                                                     self.request.host),
                                  path)

    def partial_to_session(self, next, backend, request=None, *args, **kwargs):
        return json.dumps(super(TornadoStrategy, self).partial_to_session(
            next, backend, request=request, *args, **kwargs
        ))

    def partial_from_session(self, session):
        if session:
            return super(TornadoStrategy, self).partial_to_session(
                json.loads(session)
            )
