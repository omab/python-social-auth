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
        # TODO
        pass

    def session_get(self, name, default=None):
        return self.request.cookies.get(name, default)

    def session_set(self, name, value):
        self.request_handler.cookies[name] = value

    def session_pop(self, name):
        return self.request.cookies.pop(name, None)

    def session_setdefault(self, name, value):
        return self.request_handler.cookies.setdefault(name, value)

    def build_absolute_uri(self, path=None):
        return build_absolute_uri(
            '%s://%s' % (self.request.protocol, self.request.host),
            path
        )
