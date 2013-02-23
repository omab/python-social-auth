from functools import wraps

from flask import current_app, url_for, g, request

from social.utils import setting_name
from social.strategies.utils import get_strategy


AUTHENTICATION_BACKENDS = setting_name('AUTHENTICATION_BACKENDS')

DEFAULTS = {
    'STORAGE': 'social.apps.flask_app.models.FlaskStorage',
    'STRATEGY': 'social.strategies.flask_strategy.FlaskStrategy'
}


def get_helper(name):
    return current_app.config.get(setting_name(name), DEFAULTS[name])


def strategy(redirect_uri=None):
    def decorator(func):
        @wraps(func)
        def wrapper(backend, *args, **kwargs):
            uri = redirect_uri
            if uri and not uri.startswith('/'):
                uri = url_for(uri, backend=backend)
            backends = current_app.config[AUTHENTICATION_BACKENDS]
            strategy = get_helper('STRATEGY')
            storage = get_helper('STORAGE')
            g.strategy = get_strategy(backends, strategy, storage, request,
                                      backend, redirect_uri=uri, *args,
                                      **kwargs)
            return func(backend, *args, **kwargs)
        return wrapper
    return decorator
