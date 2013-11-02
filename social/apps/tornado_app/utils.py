from functools import wraps

from social.utils import setting_name
from social.strategies.utils import get_strategy


DEFAULTS = {
    'STORAGE': 'social.apps.tornado_app.models.TornadoStorage',
    'STRATEGY': 'social.strategies.tornado_strategy.TornadoStrategy'
}


def get_helper(request_handler, name):
    return request_handler.settings.get(setting_name(name),
                                        DEFAULTS.get(name, None))


def load_strategy(request_handler, *args, **kwargs):
    backends = get_helper(request_handler, 'AUTHENTICATION_BACKENDS')
    strategy = get_helper(request_handler, 'STRATEGY')
    storage = get_helper(request_handler, 'STORAGE')
    return get_strategy(backends, strategy, storage, request_handler.request,
                        request_handler=request_handler, *args, **kwargs)


def strategy(redirect_uri=None):
    def decorator(func):
        @wraps(func)
        def wrapper(self, backend, *args, **kwargs):
            uri = redirect_uri
            if uri and not uri.startswith('/'):
                uri = self.reverse_url(uri, backend)
            self.strategy = load_strategy(self,
                                          backend=backend,
                                          redirect_uri=uri, *args, **kwargs)
            return func(self, backend, *args, **kwargs)
        return wrapper
    return decorator
