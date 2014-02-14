"""
Clef OAuth support.

This contribution adds support for Clef OAuth service. The settings
SOCIAL_AUTH_CLEF_KEY and SOCIAL_AUTH_CLEF_SECRET must be defined with the values
given by Clef application registration process.
"""

import json
import urllib2
from social.backends.oauth import BaseOAuth2

class ClefOAuth2(BaseOAuth2):
    """Clef OAuth authentication backend"""
    name = 'clef'
    AUTHORIZATION_URL = 'https://clef.io/iframes/qr'
    ACCESS_TOKEN_URL = 'https://clef.io/api/v1/authorize'
    INFO_URL = 'https://clef.io/api/v1/info'
    ACCESS_TOKEN_METHOD = "POST"
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('id', 'id')
    ]

    def auth_params(self, *args, **kwargs):
        params = super(ClefOAuth2, self).auth_params(*args, **kwargs)
        params['app_id'] = params.pop('client_id')
        params['redirect_url'] = params.pop('redirect_uri')
        return params


    def get_user_details(self, response):
        """Return user details from Github account"""
        info = response.get('info')
        return {
            'username': response.get('clef_id'),
            'email': info.get('email', ''),
            'first_name': info.get('first_name'),
            'last_name': info.get('last_name'),
            'phone_number': info.get('phone_number', '')
        }

    def user_data(self, access_token, *args, **kwargs):
        url = '%s?access_token=%s' % (self.INFO_URL, access_token)
        try:
            return json.load(urllib2.urlopen(url))
        except ValueError:
            return None
