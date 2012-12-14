from urlparse import urlparse
from functools import wraps

from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from social.utils import module_member, setting_name
from social.backends.utils import get_backend


BACKENDS = settings.AUTHENTICATION_BACKENDS
STRATEGY = getattr(settings, setting_name('STRATEGY'))
STORAGE = getattr(settings, setting_name('STORAGE'))


def get_strategy(request, backend, redirect_uri=None, *args, **kwargs):
    Backend = get_backend(BACKENDS, backend)
    if not Backend:
        raise ValueError('Missing backend entry')
    Strategy = module_member(STRATEGY)
    Storage = module_member(STORAGE)

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
    return getattr(settings, setting_name(name), default)


def sanitize_redirect(host, redirect_to):
    """
    Given the hostname and an untrusted URL to redirect to,
    this method tests it to make sure it isn't garbage/harmful
    and returns it, else returns None, similar as how's it done
    on django.contrib.auth.views.

    >>> print sanitize_redirect('myapp.com', None)
    None
    >>> print sanitize_redirect('myapp.com', '')
    None
    >>> print sanitize_redirect('myapp.com', {})
    None
    >>> print sanitize_redirect('myapp.com', 'http://notmyapp.com/path/')
    None
    >>> print sanitize_redirect('myapp.com', 'http://myapp.com/path/')
    http://myapp.com/path/
    >>> print sanitize_redirect('myapp.com', '/path/')
    /path/
    """
    # Quick sanity check.
    if not redirect_to:
        return None

    # Heavier security check, don't allow redirection to a different host.
    try:
        netloc = urlparse(redirect_to)[1]
    except TypeError:  # not valid redirect_to value
        return None
    if netloc and netloc != host:
        return None
    return redirect_to


class BackendWrapper(object):
    def get_user(self, user_id):
        Strategy = module_member(STRATEGY)
        Storage = module_member(STORAGE)
        strategy = Strategy(storage=Storage)
        return strategy.get_user(user_id)
