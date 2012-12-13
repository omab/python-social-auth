import sys
import urlparse
import urllib
from cgi import parse_qsl
from datetime import timedelta, tzinfo

from oauth2 import Consumer as OAuthConsumer, Request as OAuthRequest, \
                   SignatureMethod_HMAC_SHA1, HTTP_METHOD


def import_module(name):
    __import__(name)
    return sys.modules[name]


def url_add_parameters(url, params):
    """Adds parameters to URL, parameter will be repeated if already present"""
    if params:
        fragments = list(urlparse.urlparse(url))
        fragments[4] = urllib.urlencode(parse_qsl(fragments[4]) +
                                        params.items())
        url = urlparse.urlunparse(fragments)
    return url


def build_consumer_oauth_request(backend, token, url, redirect_uri='/',
                                 oauth_verifier=None, extra_params=None,
                                 method=HTTP_METHOD):
    """Builds a Consumer OAuth request."""
    params = {'oauth_callback': redirect_uri}
    if extra_params:
        params.update(extra_params)

    if oauth_verifier:
        params['oauth_verifier'] = oauth_verifier

    consumer = OAuthConsumer(*backend.get_key_and_secret())
    request = OAuthRequest.from_consumer_and_token(consumer,
                                                   token=token,
                                                   http_method=method,
                                                   http_url=url,
                                                   parameters=params)
    request.sign_request(SignatureMethod_HMAC_SHA1(), consumer, token)
    return request


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
