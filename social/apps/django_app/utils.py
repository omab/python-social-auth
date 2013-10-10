from functools import wraps

from django.conf import settings
from django.core.urlresolvers import reverse

from social.utils import setting_name, module_member
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
            request.strategy = load_strategy(request=request, backend=backend,
                                             redirect_uri=uri, *args, **kwargs)
            return func(request, backend, *args, **kwargs)
        return wrapper
    return decorator


def setting(name, default=None):
    try:
        return getattr(settings, setting_name(name))
    except AttributeError:
        return getattr(settings, name, default)


class BackendWrapper(object):
    # This backends doesn't authenticate, it's just a wrapper to return the
    # user by the given ID, the user was already authenticated by a previous
    # backend but since Django 1.6 will enforce backends to be defined on
    # AUTHENTICATION_BACKENDS (which is not a bad idea) this wrapper needs to
    # be added the setting, until a better solution is found this backends must
    # be added to the setting, check:
    #   https://github.com/omab/python-social-auth/issues/53
    def authenticate(self, *args, **kwargs):
        return None

    def get_user(self, user_id):
        return Strategy(storage=Storage).get_user(user_id)
