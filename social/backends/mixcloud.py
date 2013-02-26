"""
Mixcloud OAuth2 support
"""
import json
from urllib import urlencode
from urllib2 import Request

from social.backends.oauth import BaseOAuth2


class MixcloudOAuth2(BaseOAuth2):
    name = 'mixcloud'
    ID_KEY = 'username'
    AUTHORIZATION_URL = 'https://www.mixcloud.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://www.mixcloud.com/oauth/access_token'

    def get_user_details(self, response):
        return {'username': response['username'],
                'email': None,
                'fullname': response['name'],
                'first_name': None,
                'last_name': None}

    def user_data(self, access_token, *args, **kwargs):
        request = Request('https://api.mixcloud.com/me/?' + urlencode({
            'access_token': access_token,
            'alt': 'json'
        }))
        try:
            return json.loads(self.urlopen(request).read())
        except (ValueError, KeyError, IOError):
            return None
