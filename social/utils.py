import re
import sys
import unicodedata
import six
import collections

from social.p3 import urlparse, urlunparse, urlencode, \
                      parse_qs as battery_parse_qs


SETTING_PREFIX = 'SOCIAL_AUTH'


def import_module(name):
    __import__(name)
    return sys.modules[name]


def module_member(name):
    mod, member = name.rsplit('.', 1)
    module = import_module(mod)
    return getattr(module, member)


def url_add_parameters(url, params):
    """Adds parameters to URL, parameter will be repeated if already present"""
    if params:
        fragments = list(urlparse(url))
        value = parse_qs(fragments[4])
        value.update(params)
        fragments[4] = urlencode(value)
        url = urlunparse(fragments)
    return url


def to_setting_name(*names):
    return '_'.join([name.upper().replace('-', '_') for name in names if name])


def setting_name(*names):
    return to_setting_name(*((SETTING_PREFIX,) + names))


def sanitize_redirect(host, redirect_to):
    """
    Given the hostname and an untrusted URL to redirect to,
    this method tests it to make sure it isn't garbage/harmful
    and returns it, else returns None, similar as how's it done
    on django.contrib.auth.views.
    """
    # Quick sanity check.
    if not redirect_to or not isinstance(redirect_to, six.string_types):
        return None

    # Heavier security check, don't allow redirection to a different host.
    netloc = urlparse(redirect_to)[1]
    if netloc and netloc != host:
        return None
    return redirect_to


def user_is_authenticated(user):
    if user and hasattr(user, 'is_authenticated'):
        if isinstance(user.is_authenticated, collections.Callable):
            authenticated = user.is_authenticated()
        else:
            authenticated = user.is_authenticated
    elif user:
        authenticated = True
    else:
        authenticated = False
    return authenticated


def user_is_active(user):
    if user and hasattr(user, 'is_active'):
        if isinstance(user.is_active, collections.Callable):
            is_active = user.is_active()
        else:
            is_active = user.is_active
    elif user:
        is_active = True
    else:
        is_active = False
    return is_active


# This slugify version was borrowed from django revision a61dbd6
def slugify(value):
    """Converts to lowercase, removes non-word characters (alphanumerics
    and underscores) and converts spaces to hyphens. Also strips leading
    and trailing whitespace."""
    value = unicodedata.normalize('NFKD', value) \
                       .encode('ascii', 'ignore') \
                       .decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)


def first(func, items):
    """Return the first item in the list for what func returns True"""
    for item in items:
        if func(item):
            return item


def parse_qs(value):
    """Like urlparse.parse_qs but transform list values to single items"""
    return drop_lists(battery_parse_qs(value))


def drop_lists(value):
    out = {}
    for key, val in value.items():
        val = val[0]
        if isinstance(key, six.binary_type):
            key = six.text_type(key, 'utf-8')
        if isinstance(val, six.binary_type):
            val = six.text_type(val, 'utf-8')
        out[key] = val
    return out


def partial_pipeline_data(strategy, user, *args, **kwargs):
    partial = strategy.session_get('partial_pipeline', None)
    if partial is not None:
        idx, backend, xargs, xkwargs = strategy.from_session(partial)
        kwargs = kwargs.copy()
        kwargs.setdefault('user', user)
        kwargs.setdefault('request', strategy.request)
        kwargs.update(xkwargs)
        return idx, backend, xargs, xkwargs
