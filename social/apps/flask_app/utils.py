from functools import wraps

from flask import current_app, url_for, g, request

from social.utils import module_member, setting_name
from social.strategies.utils import get_strategy


DEFAULTS = {
    'STORAGE': 'social.apps.flask_app.models.FlaskStorage',
    'STRATEGY': 'social.strategies.flask_strategy.FlaskStrategy'
}


def get_helper(name, do_import=False):
    config = current_app.config.get(setting_name(name),
                                    DEFAULTS.get(name, None))
    return do_import and module_member(config) or config


def load_strategy(*args, **kwargs):
    backends = get_helper('AUTHENTICATION_BACKENDS')
    strategy = get_helper('STRATEGY')
    storage = get_helper('STORAGE')
    return get_strategy(backends, strategy, storage, *args, **kwargs)


def strategy(redirect_uri=None):
    def decorator(func):
        @wraps(func)
        def wrapper(backend, *args, **kwargs):
            uri = redirect_uri
            if uri and not uri.startswith('/'):
                uri = url_for(uri, backend=backend)
            g.strategy = load_strategy(request=request, backend=backend,
                                       redirect_uri=uri, *args, **kwargs)
            return func(backend, *args, **kwargs)
        return wrapper
    return decorator
