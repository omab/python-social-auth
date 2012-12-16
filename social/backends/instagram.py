import json
from urllib import urlencode

from social.backends.oauth import BaseOAuth2


class InstagramOAuth2(BaseOAuth2):
    name = 'instagram'
    AUTHORIZATION_URL = 'https://instagram.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://instagram.com/oauth/access_token'

    def get_user_id(self, details, response):
        return response['user']['id']

    def get_user_details(self, response):
        """Return user details from Instagram account"""
        username = response['user']['username']
        fullname = response['user'].get('fullname', '')
        email = response['user'].get('email', '')
        return {'username': username,
                'first_name': fullname,
                'email': email}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://api.instagram.com/v1/users/self?' + urlencode({
            'access_token': access_token
        })
        try:
            return json.load(self.urlopen(url))
        except ValueError:
            return None


BACKENDS = {
    'instagram': InstagramOAuth2,
}
