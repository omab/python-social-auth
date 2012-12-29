from functools import wraps

from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from social.utils import module_member, setting_name
from social.backends.utils import get_backend


BACKENDS = settings.AUTHENTICATION_BACKENDS
Strategy = module_member(getattr(settings, setting_name('STRATEGY'),
                                 'social.strategies.dj.DjangoStrategy'))
Storage = module_member(getattr(settings, setting_name('STORAGE'),
                                'social.apps.dj.default.models.DjangoStorage'))


def get_strategy(request, backend, redirect_uri=None, *args, **kwargs):
    Backend = get_backend(BACKENDS, backend)
    if not Backend:
        raise ValueError('Missing backend entry')
    uri = redirect_uri
    if uri and not uri.startswith('/'):
        uri = reverse(uri, args=(backend,))
    return Strategy(Backend, Storage, request,
                    redirect_uri=uri, *args, **kwargs)


def strategy(redirect_uri=None):
    def decorator(func):
        @wraps(func)
        def wrapper(request, backend, *args, **kwargs):
            request.strategy = get_strategy(request, backend, redirect_uri,
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
