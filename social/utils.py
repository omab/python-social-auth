import re
import sys
import unicodedata
import six
import collections

from cgi import parse_qsl
from datetime import timedelta, tzinfo

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
        fragments[4] = urlencode(parse_qsl(fragments[4]) +
                                 list(params.items()))
        url = urlunparse(fragments)
    return url


class UTC(tzinfo):
    """UTC implementation taken from django 1.4."""
    def __repr__(self):
        return '<UTC>'

    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return 'UTC'

    def dst(self, dt):
        return timedelta(0)

utc = UTC()


def setting_name(*names):
    return '_'.join((SETTING_PREFIX,) + tuple(names))


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
