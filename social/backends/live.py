"""
MSN Live Connect oAuth 2.0

Settings:
LIVE_CLIENT_ID
LIVE_CLIENT_SECRET
LIVE_EXTENDED_PERMISSIONS (defaults are: wl.basic, wl.emails)

References:
* oAuth  http://msdn.microsoft.com/en-us/library/live/hh243649.aspx
* Scopes http://msdn.microsoft.com/en-us/library/live/hh243646.aspx
* REST   http://msdn.microsoft.com/en-us/library/live/hh243648.aspx

Throws:
AuthUnknownError - if user data retrieval fails
"""
import json
from urllib import urlencode

from social.backends.oauth import BaseOAuth2
from social.exceptions import AuthUnknownError


class LiveOAuth2(BaseOAuth2):
    name = 'live'
    AUTHORIZATION_URL = 'https://login.live.com/oauth20_authorize.srf'
    ACCESS_TOKEN_URL = 'https://login.live.com/oauth20_token.srf'
    SCOPE_SEPARATOR = ','
    DEFAULT_SCOPE = ['wl.basic', 'wl.emails']

    EXTRA_DATA = [
        ('id', 'id'),
        ('access_token', 'access_token'),
        ('reset_token', 'reset_token'),
        ('expires', 'expires'),
        ('email', 'email'),
        ('first_name', 'first_name'),
        ('last_name', 'last_name'),
    ]

    def get_user_details(self, response):
        """Return user details from Live Connect account"""
        try:
            email = response['emails']['account']
        except KeyError:
            email = ''
        return {'username': response.get('name'),
                'email': email,
                'first_name': response.get('first_name'),
                'last_name': response.get('last_name')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://apis.live.net/v5.0/me?' + urlencode({
            'access_token': access_token
        })
        try:
            return json.load(self.urlopen(url))
        except (ValueError, IOError):
            raise AuthUnknownError('Error during profile retrieval, '
                                   'please, try again later')
