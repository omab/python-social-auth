import six
import cherrypy

from social.strategies.base import BaseStrategy, BaseTemplateStrategy


class CherryPyJinja2TemplateStrategy(BaseTemplateStrategy):
    def __init__(self, strategy):
        self.strategy = strategy
        self.env = cherrypy.tools.jinja2env

    def render_template(self, tpl, context):
        return self.env.get_template(tpl).render(context)

    def render_string(self, html, context):
        return self.env.from_string(html).render(context)


class CherryPyStrategy(BaseStrategy):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('tpl', CherryPyJinja2TemplateStrategy)
        return super(CherryPyStrategy, self).__init__(*args, **kwargs)

    def get_setting(self, name):
        return cherrypy.config[name]

    def request_data(self, merge=True):
        if merge:
            data = cherrypy.request.params
        elif cherrypy.request.method == 'POST':
            data = cherrypy.body.params
        else:
            data = cherrypy.request.params
        return data

    def request_host(self):
        return cherrypy.request.base

    def redirect(self, url):
        raise cherrypy.HTTPRedirect(url)

    def html(self, content):
        return content

    def authenticate(self, *args, **kwargs):
        kwargs['strategy'] = self
        kwargs['storage'] = self.storage
        kwargs['backend'] = self.backend
        return self.backend.authenticate(*args, **kwargs)

    def session_get(self, name, default=None):
        return cherrypy.session.get(name, default)

    def session_set(self, name, value):
        cherrypy.session[name] = value

    def session_pop(self, name):
        cherrypy.session.pop(name, None)

    def session_setdefault(self, name, value):
        return cherrypy.session.setdefault(name, value)

    def build_absolute_uri(self, path=None):
        return cherrypy.url(path or '')

    def is_response(self, value):
        return isinstance(value, six.string_types) or \
               isinstance(value, cherrypy.CherryPyException)
