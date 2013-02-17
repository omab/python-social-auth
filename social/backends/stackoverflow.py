"""
Stackoverflow OAuth support.

This contribution adds support for Stackoverflow OAuth service. The settings
SOCIAL_AUTH_STACKOVERFLOW_CLIENT_ID, STACKOVERFLOW_CLIENT_SECRET and
STACKOVERFLOW_CLIENT_SECRET must be defined with the values given by
Stackoverflow application registration process.

Extended permissions are supported by defining
STACKOVERFLOW_EXTENDED_PERMISSIONS setting, it must be a list of values
to request.

By default account id and token expiration time are stored in extra_data
field, check OAuthBackend class for details on how to extend it.
"""
import json
from urllib import urlencode
from urllib2 import Request, HTTPError
from urlparse import parse_qsl
from gzip import GzipFile
from StringIO import StringIO

from social.backends.oauth import BaseOAuth2
from social.exceptions import AuthUnknownError, AuthCanceled


class StackoverflowOAuth2(BaseOAuth2):
    """Stackoverflow OAuth2 authentication backend"""
    name = 'stackoverflow'
    ID_KEY = 'user_id'
    AUTHORIZATION_URL = 'https://stackexchange.com/oauth'
    ACCESS_TOKEN_URL = 'https://stackexchange.com/oauth/access_token'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from Stackoverflow account"""
        return {'username': response.get('link').rsplit('/', 1)[-1],
                'full_name': response.get('display_name')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://api.stackexchange.com/2.1/me?' + urlencode({
            'site': 'stackoverflow',
            'access_token': access_token,
            'key': self.settings('KEY')
        })

        opener = self.urlopen(url)
        if opener.headers.get('content-encoding') == 'gzip':
            """Stackoverflow doesn't respect no gzip header"""
            gzip = GzipFile(fileobj=StringIO(opener.read()), mode='r')
            response = gzip.read()
        else:
            response = opener.read()
        try:
            return json.loads(response)['items'][0]
        except (ValueError, TypeError):
            return None

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        self.process_error(self.data)
        params = self.auth_complete_params(self.validate_state())
        request = Request(self.ACCESS_TOKEN_URL, data=urlencode(params),
                          headers=self.auth_headers())

        try:
            response = dict(parse_qsl(self.urlopen(request).read()))
        except HTTPError, e:
            if e.code == 400:
                raise AuthCanceled(self)
            else:
                raise
        except (ValueError, KeyError):
            raise AuthUnknownError(self)

        self.process_error(response)
        return self.do_auth(response['access_token'], response=response,
                            *args, **kwargs)


BACKENDS = {
    'stackoverflow': StackoverflowOAuth2
}
