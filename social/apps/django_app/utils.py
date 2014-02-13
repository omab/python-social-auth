from functools import wraps

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404

from social.utils import setting_name, module_member
from social.exceptions import MissingBackend
from social.strategies.utils import get_strategy


BACKENDS = settings.AUTHENTICATION_BACKENDS
STRATEGY = getattr(settings, setting_name('STRATEGY'),
                   'social.strategies.django_strategy.DjangoStrategy')
STORAGE = getattr(settings, setting_name('STORAGE'),
                  'social.apps.django_app.default.models.DjangoStorage')
Strategy = module_member(STRATEGY)
Storage = module_member(STORAGE)


def load_strategy(*args, **kwargs):
    return get_strategy(BACKENDS, STRATEGY, STORAGE, *args, **kwargs)


def strategy(redirect_uri=None, load_strategy=load_strategy):
    def decorator(func):
        @wraps(func)
        def wrapper(request, backend, *args, **kwargs):
            uri = redirect_uri
            if uri and not uri.startswith('/'):
                uri = reverse(redirect_uri, args=(backend,))

            try:
                request.social_strategy = load_strategy(
                    request=request, backend=backend,
                    redirect_uri=uri, *args, **kwargs
                )
            except MissingBackend:
                raise Http404('Backend not found')

            # backward compatibility in attribute name, only if not already
            # defined
            if not hasattr(request, 'strategy'):
                request.strategy = request.social_strategy
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
