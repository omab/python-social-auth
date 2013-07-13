import pickle
from flask import current_app, request, redirect, make_response, session, \
                  render_template, render_template_string

from social.strategies.base import BaseStrategy, BaseTemplateStrategy


class FlaskTemplateStrategy(BaseTemplateStrategy):
    def render_template(self, tpl, context):
        return render_template(tpl, **context)

    def render_string(self, html, context):
        return render_template_string(html, **context)


class FlaskStrategy(BaseStrategy):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('tpl', FlaskTemplateStrategy)
        super(FlaskStrategy, self).__init__(*args, **kwargs)

    def get_setting(self, name):
        return current_app.config[name]

    def request_data(self, merge=True):
        if merge:
            data = request.form.copy()
            data.update(request.args)
        elif request.method == 'POST':
            data = request.form
        else:
            data = request.args
        return data

    def request_host(self):
        return request.host

    def redirect(self, url):
        return redirect(url)

    def html(self, content):
        response = make_response(content)
        response.headers['Content-Type'] = 'text/html;charset=UTF-8'
        return response

    def session_get(self, name, default=None):
        return session.get(name, default)

    def session_set(self, name, value):
        session[name] = value

    def session_pop(self, name):
        session.pop(name, None)

    def session_setdefault(self, name, value):
        return SessionWrapper(session.setdefault(name, value))

    def build_absolute_uri(self, path=None):
        path = path or ''
        if path.startswith('http://') or path.startswith('https://'):
            return path
        if request.host_url.endswith('/') and path.startswith('/'):
            path = path[1:]
        return request.host_url + (path or '')


class SessionWrapper(object):
    name_mapping = {
        '_yadis_services__openid_consumer_':    'yoc',
        '_openid_consumer_last_token':          'lt'
    }

    def __init__(self, ext):
        self.ext = ext

    def __getitem__(self, name):
        rv = session[self.name_mapping.get(name, name)]
        if isinstance(rv, dict) and len(rv) == 1 and ' p' in rv:
            return pickle.loads(rv[' p'])
        return rv

    def __setitem__(self, name, value):
        if not getattr(current_app.session_interface, 'pickle_based', True):
            value = {' p': pickle.dumps(value, 0)}
        session[self.name_mapping.get(name, name)] = value

    def __delitem__(self, name):
        del session[self.name_mapping.get(name, name)]

    def get(self, name, default=None):
        try:
            return self[name]
        except KeyError:
            return default

    def __contains__(self, name):
        try:
            self[name]
            return True
        except KeyError:
            return False
