from webob.multidict import NoVars

from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render

from social.utils import build_absolute_uri
from social.strategies.base import BaseStrategy, BaseTemplateStrategy


class PyramidTemplateStrategy(BaseTemplateStrategy):
    def render_template(self, tpl, context):
        return render(tpl, context, request=self.strategy.request)

    def render_string(self, html, context):
        return render(html, context, request=self.strategy.request)


class PyramidStrategy(BaseStrategy):
    def redirect(self, url):
        """Return a response redirect to the given URL"""
        return HTTPFound(location=url)

    def get_setting(self, name):
        """Return value for given setting name"""
        return self.request.registry.settings[name]

    def html(self, content):
        """Return HTTP response with given content"""
        return Response(body=content)

    def request_data(self, merge=True):
        """Return current request data (POST or GET)"""
        if self.request.method == 'POST':
            if merge:
                data = self.request.POST.copy()
                if not isinstance(self.request.GET, NoVars):
                    data.update(self.request.GET)
            else:
                data = self.request.POST
        else:
            data = self.request.GET
        return data

    def request_host(self):
        """Return current host value"""
        return self.request.host

    def session_get(self, name, default=None):
        """Return session value for given key"""
        return self.request.session.get(name, default)

    def session_set(self, name, value):
        """Set session value for given key"""
        self.request.session[name] = value

    def session_pop(self, name):
        """Pop session value for given key"""
        return self.request.session.pop(name, None)

    def build_absolute_uri(self, path=None):
        """Build absolute URI with given (optional) path"""
        return build_absolute_uri(self.request.host_url, path)
