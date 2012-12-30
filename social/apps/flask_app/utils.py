from functools import wraps

from flask import current_app, url_for, g, request

from social.backends.utils import get_backend
from social.utils import module_member, setting_name


def get_strategy(backend, redirect_uri=None, *args, **kwargs):
    backends = current_app.config[setting_name('AUTHENTICATION_BACKENDS')]
    Backend = get_backend(backends, backend)
    if not Backend:
        raise ValueError('Missing backend entry')

    Strategy = module_member(current_app.config.get(setting_name('STRATEGY'),
                             'social.strategies.flask_strategy.FlaskStrategy'))
    Storage = module_member(current_app.config.get(setting_name('STORAGE'),
                             'social.apps.flask_app.models.FlaskStorage'))

    uri = redirect_uri
    if uri and not uri.startswith('/'):
        uri = url_for(uri, backend=backend)
    return Strategy(Backend, Storage, request,
                    redirect_uri=uri, *args, **kwargs)


def strategy(redirect_uri=None):
    def decorator(func):
        @wraps(func)
        def wrapper(backend, *args, **kwargs):
            g.strategy = get_strategy(backend, redirect_uri, *args, **kwargs)
            return func(backend, *args, **kwargs)
        return wrapper
    return decorator
