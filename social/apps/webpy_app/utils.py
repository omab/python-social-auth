import web

from functools import wraps

from social.utils import setting_name
from social.strategies.utils import get_strategy


def strategy(redirect_uri=None):
    def decorator(func):
        @wraps(func)
        def wrapper(self, backend=None, *args, **kwargs):
            uri = redirect_uri

            if uri and backend and '%(backend)s' in uri:
                uri = uri % {'backend': backend}

            backends = web.config[setting_name('AUTHENTICATION_BACKENDS')]
            strategy = web.config.get(
                setting_name('STRATEGY'),
                'social.strategies.webpy_strategy.WebpyStrategy'
            )
            storage = web.config.get(
                setting_name('STORAGE'),
                'social.apps.webpy_app.models.WebpyStorage'
            )
            self.strategy = get_strategy(backends, strategy, storage, web.ctx,
                                         backend, redirect_uri=uri, *args,
                                         **kwargs)
            if backend:
                return func(self, backend=backend, *args, **kwargs)
            else:
                return func(self, *args, **kwargs)
        return wrapper
    return decorator
