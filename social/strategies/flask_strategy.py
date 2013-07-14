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
        return session.setdefault(name, value)

    def openid_session_dict(self, name):
        # Since Flask 0.10, session is serialized with JSON instead of pickle,
        # sadly python-openid stores classes instances in the session which
        # fails the JSON serialization, these classes are:
        #   openid.yadis.manager.YadisServiceManager
        #   openid.consumer.discover.OpenIDServiceEndpoint
        #
        # This method will return a wrapper over the session value used with
        # openid (a dict) which will automatically keep a pickled value
        #
        # current_app.session_interface has a pickle_based=False attribute if
        # Flask >= 0.10
        value = super(FlaskStrategy, self).openid_session_value(name)
        if not getattr(current_app.session_interface, 'pickle_based', True):
            value = OpenIdSessionWrapper(value)
        return value

    def build_absolute_uri(self, path=None):
        path = path or ''
        if path.startswith('http://') or path.startswith('https://'):
            return path
        if request.host_url.endswith('/') and path.startswith('/'):
            path = path[1:]
        return request.host_url + (path or '')


class OpenIdSessionWrapper(dict):
    pickle_instances = (
        '_yadis_services__openid_consumer_',
        '_openid_consumer_last_token'
    )

    def __getitem__(self, name):
        value = super(OpenIdSessionWrapper, self).__getitem__(name)
        if name in self.pickle_instances:
            value = pickle.loads(value)
        return value

    def __setitem__(self, name, value):
        if name in self.pickle_instances:
            value = pickle.dumps(value, 0)
        super(OpenIdSessionWrapper, self).__setitem__(name, value)

    def get(self, name, default=None):
        try:
            return self[name]
        except KeyError:
            return default
