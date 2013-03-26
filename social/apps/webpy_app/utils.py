import web

from functools import wraps

from social.utils import setting_name, module_member
from social.backends.utils import user_backends_data
from social.strategies.utils import get_strategy


DEFAULTS = {
    'STRATEGY': 'social.strategies.webpy_strategy.WebpyStrategy',
    'STORAGE': 'social.apps.webpy_app.models.WebpyStorage'
}


def get_helper(name, do_import=False):
    config = web.config.get(setting_name(name),
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
        def wrapper(self, backend=None, *args, **kwargs):
            uri = redirect_uri
            if uri and backend and '%(backend)s' in uri:
                uri = uri % {'backend': backend}
            self.strategy = load_strategy(request=web.ctx, backend=backend,
                                          redirect_uri=uri, *args, **kwargs)
            if backend:
                return func(self, backend=backend, *args, **kwargs)
            else:
                return func(self, *args, **kwargs)
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
