import cherrypy

from functools import wraps

from social.utils import setting_name, module_member
from social.strategies.utils import get_strategy
from social.backends.utils import user_backends_data


DEFAULTS = {
    'STRATEGY': 'social.strategies.cherrypy_strategy.CherryPyStrategy',
    'STORAGE': 'social.apps.cherrypy_app.models.CherryPyStorage'
}


def get_helper(name, do_import=False):
    config = cherrypy.config.get(setting_name(name), DEFAULTS.get(name, None))
    return do_import and module_member(config) or config


def strategy(redirect_uri=None):
    def decorator(func):
        @wraps(func)
        def wrapper(self, backend=None, *args, **kwargs):
            uri = redirect_uri

            if uri and backend and '%(backend)s' in uri:
                uri = uri % {'backend': backend}

            backends = get_helper('AUTHENTICATION_BACKENDS')
            strategy = get_helper('STRATEGY')
            storage = get_helper('STORAGE')
            self.strategy = get_strategy(backends, strategy, storage,
                                         cherrypy.request, backend,
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
