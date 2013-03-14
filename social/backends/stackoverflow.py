"""
Stackoverflow OAuth support.

This contribution adds support for Stackoverflow OAuth service. The settings
SOCIAL_AUTH_STACKOVERFLOW_KEY, SOCIAL_AUTH_STACKOVERFLOW_SECRET and
SOCIAL_AUTH_STACKOVERFLOW_API_KEY must be defined with the values given by
Stackoverflow application registration process.

Extended permissions are supported by defining SOCIAL_AUTH_STACKOVERFLOW_SCOPE
setting, it must be a list of values to request.

By default account id and token expiration time are stored in extra_data
field, check OAuthBackend class for details on how to extend it.
"""
import json

from gzip import GzipFile

from requests import HTTPError

from social.p3 import StringIO
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
        opener = self.request('https://api.stackexchange.com/2.1/me', params={
            'site': 'stackoverflow',
            'access_token': access_token,
            'key': self.settings('API_KEY')
        })
        if opener.headers.get('content-encoding') == 'gzip':
            # Stackoverflow doesn't respect no gzip header
            gzip = GzipFile(fileobj=StringIO(opener.content), mode='r')
            response = gzip.read()
        else:
            response = opener.content
        try:
            return json.loads(response)['items'][0]
        except (ValueError, TypeError):
            return None

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        self.process_error(self.data)
        try:
            response = dict(
                self.get_querystring(
                    self.ACCESS_TOKEN_URL,
                    params=self.auth_complete_params(self.validate_state()),
                    headers=self.auth_headers()
                )
            )
        except HTTPError as err:
            if err.response.status_code == 400:
                raise AuthCanceled(self)
            else:
                raise
        except (ValueError, KeyError):
            raise AuthUnknownError(self)

        self.process_error(response)
        return self.do_auth(response['access_token'], response=response,
                            *args, **kwargs)
