from flask import current_app, request, redirect, make_response, session, \
                  render_template, render_template_string

from social.strategies.base import BaseStrategy


class FlaskStrategy(BaseStrategy):
    def get_setting(self, name):
        return current_app.config[name]

    def request_data(self):
        data = request.form.copy()
        data.update(request.args)
        return data

    def request_host(self):
        return request.host

    def redirect(self, url):
        return redirect(url)

    def html(self, content):
        response = make_response(content)
        response.headers['Content-Type'] = 'text/html;charset=UTF-8'
        return response

    def render_html(self, tpl=None, html=None, context=None):
        if not tpl and not html:
            raise ValueError('Missing template or html parameters')
        context = context or {}
        if tpl:
            return render_template(tpl, **context)
        else:
            return render_template_string(html, **context)

    def authenticate(self, *args, **kwargs):
        kwargs['strategy'] = self
        kwargs['storage'] = self.storage
        kwargs['backend'] = self.backend
        return self.backend.authenticate(*args, **kwargs)

    def session_get(self, name, default=None):
        return session.get(name, default)

    def session_set(self, name, value):
        session[name] = value

    def session_setdefault(self, name, value):
        return session.setdefault(name, value)

    def to_session(self, next, backend, *args, **kwargs):
        """Returns dict to store on session for partial pipeline."""
        return {
            'next': next,
            'backend': backend.name,
            'args': args,
            'kwargs': kwargs
        }

    def from_session(self, session):
        """Takes session saved data to continue pipeline and merges with any
        new extra argument needed. Returns tuple with next pipeline index
        entry, arguments and keyword arguments to continue the process."""
        saved_args = session['args']
        saved_kwargs = session['kwargs']
        return session['next'], saved_args, saved_kwargs

    def build_absolute_uri(self, path=None):
        path = path or ''
        if request.host_url.endswith('/') and path.startswith('/'):
            path = path[1:]
        return request.host_url + (path or '')

    def clean_partial_pipeline(self):
        session.pop('partial_pipeline', None)
