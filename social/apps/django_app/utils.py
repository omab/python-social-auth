from functools import wraps

from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from social.utils import setting_name, module_member
from social.strategies.utils import get_strategy


BACKENDS = settings.AUTHENTICATION_BACKENDS
STRATEGY = getattr(settings, setting_name('STRATEGY'),
                   'social.strategies.django_strategy.DjangoStrategy')
STORAGE = getattr(settings, setting_name('STORAGE'),
                  'social.apps.django_app.default.models.DjangoStorage')
Strategy = module_member(STRATEGY)
Storage = module_member(STORAGE)


def strategy(redirect_uri=None):
    def decorator(func):
        @wraps(func)
        def wrapper(request, backend, *args, **kwargs):
            uri = redirect_uri
            if uri and not uri.startswith('/'):
                uri = reverse(redirect_uri, args=(backend,))
            request.strategy = get_strategy(BACKENDS, STRATEGY, STORAGE,
                                            request, backend, redirect_uri=uri,
                                            *args, **kwargs)
            return func(request, backend, *args, **kwargs)
        return wrapper
    return decorator


def disconnect_view(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    if setting('FORCE_POST_DISCONNECT'):
        wrapper = require_POST(csrf_protect(wrapper))
    return wrapper


def setting(name, default=None):
    try:
        return getattr(settings, setting_name(name))
    except AttributeError:
        return getattr(settings, name, default)


class BackendWrapper(object):
    def get_user(self, user_id):
        return Strategy(storage=Storage).get_user(user_id)
