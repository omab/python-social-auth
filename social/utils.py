import re
import sys
import unicodedata
import collections
import functools
import logging

import six
import requests
import social

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

from social.exceptions import AuthCanceled, AuthUnreachableProvider
from social.p3 import urlparse, urlunparse, urlencode, \
                      parse_qs as battery_parse_qs


SETTING_PREFIX = 'SOCIAL_AUTH'

social_logger = logging.getLogger('social')


class SSLHttpAdapter(HTTPAdapter):
    """"
    Transport adapter that allows to use any SSL protocol. Based on:
    http://requests.rtfd.org/latest/user/advanced/#example-specific-ssl-version
    """
    def __init__(self, ssl_protocol):
        self.ssl_protocol = ssl_protocol
        super(SSLHttpAdapter, self).__init__()

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=self.ssl_protocol
        )

    @classmethod
    def ssl_adapter_session(cls, ssl_protocol):
        session = requests.Session()
        session.mount('https://', SSLHttpAdapter(ssl_protocol))
        return session


def import_module(name):
    __import__(name)
    return sys.modules[name]


def module_member(name):
    mod, member = name.rsplit('.', 1)
    module = import_module(mod)
    return getattr(module, member)


def user_agent():
    """Builds a simple User-Agent string to send in requests"""
    return 'python-social-auth-' + social.__version__


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
    if redirect_to:
        try:
            # Don't redirect to a different host
            netloc = urlparse(redirect_to)[1] or host
        except (TypeError, AttributeError):
            pass
        else:
            if netloc == host:
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


def partial_pipeline_data(backend, user=None, *args, **kwargs):
    partial = backend.strategy.session_get('partial_pipeline', None)
    if partial:
        idx, backend_name, xargs, xkwargs = \
            backend.strategy.partial_from_session(partial)
        if backend_name == backend.name:
            kwargs.setdefault('pipeline_index', idx)
            if user:  # don't update user if it's None
                kwargs.setdefault('user', user)
            kwargs.setdefault('request', backend.strategy.request_data())
            xkwargs.update(kwargs)
            return xargs, xkwargs
        else:
            backend.strategy.clean_partial_pipeline()


def build_absolute_uri(host_url, path=None):
    """Build absolute URI with given (optional) path"""
    path = path or ''
    if path.startswith('http://') or path.startswith('https://'):
        return path
    if host_url.endswith('/') and path.startswith('/'):
        path = path[1:]
    return host_url + path


def constant_time_compare(val1, val2):
    """
    Returns True if the two strings are equal, False otherwise.
    The time taken is independent of the number of characters that match.
    This code was borrowed from Django 1.5.4-final
    """
    if len(val1) != len(val2):
        return False
    result = 0
    if six.PY3 and isinstance(val1, bytes) and isinstance(val2, bytes):
        for x, y in zip(val1, val2):
            result |= x ^ y
    else:
        for x, y in zip(val1, val2):
            result |= ord(x) ^ ord(y)
    return result == 0


def is_url(value):
    return value and \
           (value.startswith('http://') or
            value.startswith('https://') or
            value.startswith('/'))


def setting_url(backend, *names):
    for name in names:
        if is_url(name):
            return name
        else:
            value = backend.setting(name)
            if is_url(value):
                return value


class CustomAuthCanceled(AuthCanceled):
    def __str__(self):
        msg = super(CustomAuthCanceled, self).__str__()
        return 'msg={msg} -\n- backend={backend} -\n- content={content}'.format(
            msg=msg,
            backend=self.backend,
            content=self.response.content,
        )



def handle_http_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            print 'OMAR', func.__name__
            return func(*args, **kwargs)
        except requests.HTTPError as err:
            print err.response.content
            # if err.response.status_code == 400:
            #     raise CustomAuthCanceled(args[0], response=err.response)
            # elif err.response.status_code == 503:
            #     raise AuthUnreachableProvider(args[0])
            # else:
            raise
    return wrapper


def append_slash(url):
    """Make sure we append a slash at the end of the URL otherwise we
    have issues with urljoin Example:
    >>> urlparse.urljoin('http://www.example.com/api/v3', 'user/1/')
    'http://www.example.com/api/user/1/'
    """
    if url and not url.endswith('/'):
        url = '{0}/'.format(url)
    return url
