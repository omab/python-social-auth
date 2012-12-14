import sys
import urlparse
import urllib
from cgi import parse_qsl
from datetime import timedelta, tzinfo


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
        fragments = list(urlparse.urlparse(url))
        fragments[4] = urllib.urlencode(parse_qsl(fragments[4]) +
                                        params.items())
        url = urlparse.urlunparse(fragments)
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
