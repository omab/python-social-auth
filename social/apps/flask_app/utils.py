import warnings

from functools import wraps

from flask import current_app, url_for, g

from social.utils import module_member, setting_name
from social.strategies.utils import get_strategy
from social.backends.utils import get_backend


DEFAULTS = {
    'STORAGE': 'social.apps.flask_app.default.models.FlaskStorage',
    'STRATEGY': 'social.strategies.flask_strategy.FlaskStrategy'
}


def get_helper(name, do_import=False):
    config = current_app.config.get(setting_name(name),
                                    DEFAULTS.get(name, None))
    return do_import and module_member(config) or config


def load_strategy():
    strategy = get_helper('STRATEGY')
    storage = get_helper('STORAGE')
    return get_strategy(strategy, storage)


def load_backend(strategy, name, redirect_uri, *args, **kwargs):
    backends = get_helper('AUTHENTICATION_BACKENDS')
    Backend = get_backend(backends, name)
    return Backend(strategy=strategy, redirect_uri=redirect_uri)


def psa(redirect_uri=None):
    def decorator(func):
        @wraps(func)
        def wrapper(backend, *args, **kwargs):
            uri = redirect_uri
            if uri and not uri.startswith('/'):
                uri = url_for(uri, backend=backend)
            g.strategy = load_strategy()
            g.backend = load_backend(g.strategy, backend, redirect_uri=uri,
                                     *args, **kwargs)
            return func(backend, *args, **kwargs)
        return wrapper
    return decorator


def strategy(*args, **kwargs):
    warnings.warn('@strategy decorator is deprecated, use @psa instead')
    return psa(*args, **kwargs)
