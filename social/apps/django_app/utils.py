import warnings

from functools import wraps

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404

from social.utils import setting_name, module_member
from social.exceptions import MissingBackend
from social.strategies.utils import get_strategy
from social.backends.utils import get_backend


BACKENDS = settings.AUTHENTICATION_BACKENDS
STRATEGY = getattr(settings, setting_name('STRATEGY'),
                   'social.strategies.django_strategy.DjangoStrategy')
STORAGE = getattr(settings, setting_name('STORAGE'),
                  'social.apps.django_app.default.models.DjangoStorage')
Strategy = module_member(STRATEGY)
Storage = module_member(STORAGE)


def load_strategy(request=None):
    return get_strategy(STRATEGY, STORAGE, request)


def load_backend(strategy, name, redirect_uri):
    Backend = get_backend(BACKENDS, name)
    return Backend(strategy, redirect_uri)


def psa(redirect_uri=None, load_strategy=load_strategy):
    def decorator(func):
        @wraps(func)
        def wrapper(request, backend, *args, **kwargs):
            uri = redirect_uri
            if uri and not uri.startswith('/'):
                uri = reverse(redirect_uri, args=(backend,))

            request.social_strategy = load_strategy(request)
            # backward compatibility in attribute name, only if not already
            # defined
            if not hasattr(request, 'strategy'):
                request.strategy = request.social_strategy

            try:
                request.backend = load_backend(request.social_strategy,
                                               backend, uri)
            except MissingBackend:
                raise Http404('Backend not found')
            return func(request, backend, *args, **kwargs)
        return wrapper
    return decorator


def setting(name, default=None):
    try:
        return getattr(settings, setting_name(name))
    except AttributeError:
        return getattr(settings, name, default)


class BackendWrapper(object):
    # XXX: Deprecated, restored to avoid session issues
    def authenticate(self, *args, **kwargs):
        return None

    def get_user(self, user_id):
        return Strategy(storage=Storage).get_user(user_id)


def strategy(*args, **kwargs):
    warnings.warn('@strategy decorator is deprecated, use @psa instead')
    return psa(*args, **kwargs)
