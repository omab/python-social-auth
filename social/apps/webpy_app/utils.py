import warnings

from functools import wraps

import web

from social.utils import setting_name, module_member
from social.backends.utils import get_backend, user_backends_data
from social.strategies.utils import get_strategy


DEFAULTS = {
    'STRATEGY': 'social.strategies.webpy_strategy.WebpyStrategy',
    'STORAGE': 'social.apps.webpy_app.models.WebpyStorage'
}


def get_helper(name, do_import=False):
    config = web.config.get(setting_name(name),
                            DEFAULTS.get(name, None))
    return do_import and module_member(config) or config


def load_strategy():
    return get_strategy(get_helper('STRATEGY'), get_helper('STORAGE'))


def load_backend(strategy, name, redirect_uri):
    backends = get_helper('AUTHENTICATION_BACKENDS')
    Backend = get_backend(backends, name)
    return Backend(strategy, redirect_uri)


def psa(redirect_uri=None):
    def decorator(func):
        @wraps(func)
        def wrapper(self, backend, *args, **kwargs):
            uri = redirect_uri
            if uri and backend and '%(backend)s' in uri:
                uri = uri % {'backend': backend}
            self.strategy = load_strategy()
            self.backend = load_backend(self.strategy, backend, uri)
            return func(self, backend, *args, **kwargs)
        return wrapper
    return decorator


def backends(user):
    """Load Social Auth current user data to context under the key 'backends'.
    Will return the output of social.backends.utils.user_backends_data."""
    return user_backends_data(user, get_helper('AUTHENTICATION_BACKENDS'),
                              get_helper('STORAGE', do_import=True))


def login_redirect():
    """Load current redirect to context."""
    method = web.ctx.method == 'POST' and 'post' or 'get'
    data = web.input(_method=method)
    value = data.get('next')
    return {
        'REDIRECT_FIELD_NAME': 'next',
        'REDIRECT_FIELD_VALUE': value,
        'REDIRECT_QUERYSTRING': value and ('next=' + value) or ''
    }


def strategy(*args, **kwargs):
    warnings.warn('@strategy decorator is deprecated, use @psa instead')
    return psa(*args, **kwargs)
