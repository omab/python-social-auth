from tornado import template

from social.utils import build_absolute_uri
from social.strategies.base import BaseStrategy, BaseTemplateStrategy


class TornadoTemplateStrategy(BaseTemplateStrategy):
    def render_template(self, tpl, context):
        dir, tpl = tpl.rsplit('/', 1)
        loader = template.Loader(dir)
        return loader.load(tpl).generate(**context)

    def render_string(self, html, context):
        tpl = template.Template(html)
        return tpl.generate(**context)


class TornadoStrategy(BaseStrategy):
    def __init__(self, request_handler, *args, **kwargs):
        kwargs.setdefault('tpl', TornadoTemplateStrategy)
        self.request_handler = request_handler
        self.request = request_handler.request
        super(TornadoStrategy, self).__init__(*args, **kwargs)

    def get_setting(self, name):
        return self.request_handler.settings[name]

    def request_data(self, merge=True):
        return self.request.arguments.copy()

    def request_host(self):
        return self.request.host

    def redirect(self, url):
        return self.request.redirect(url)

    def html(self, content):
        # TODO
        pass

    def session_get(self, name, default=None):
        return self.request.cookies.get_cookie(name, default)

    def session_set(self, name, value):
        self.request_handler.cookies.set_cookie(name, value)

    def session_pop(self, name):
        value = self.request.cookies.get_cookie(name, None)
        self.request_handler.cookies.clear_cookie(name)
        return value

    def session_setdefault(self, name, value):
        return self.request_handler.cookies.setdefault(name, value)

    def build_absolute_uri(self, path=None):
        return build_absolute_uri(
            '$s://$s' % (self.request.protocol, self.request.host),
            path
        )

