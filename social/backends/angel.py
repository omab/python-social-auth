"""
settings.py should include the following:

    ANGEL_CLIENT_ID = '...'
    ANGEL_CLIENT_SECRET = '...'

Optional scope to include 'email' and/or 'messages' separated by space:

    ANGEL_AUTH_EXTRA_ARGUMENTS = {'scope': 'email messages'}

More information on scope can be found at https://angel.co/api/oauth/faq
"""
import json
from urllib import urlencode

from social.backends.oauth import BaseOAuth2


class AngelOAuth2(BaseOAuth2):
    name = 'angel'
    AUTHORIZATION_URL = 'https://angel.co/api/oauth/authorize/'
    ACCESS_TOKEN_URL = 'https://angel.co/api/oauth/token/'
    REDIRECT_STATE = False
    STATE_PARAMETER = False

    def get_user_details(self, response):
        """Return user details from Angel account"""
        username = response['angellist_url'].split('/')[-1]
        first_name = response['name'].split(' ')[0]
        last_name = response['name'].split(' ')[-1]
        email = response.get('email', '')
        return {'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'email': email}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://api.angel.co/1/me/?' + urlencode({
            'access_token': access_token
        })
        try:
            return json.load(self.urlopen(url))
        except ValueError:
            return None
