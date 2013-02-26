"""
Dropbox OAuth support.

This contribution adds support for Dropbox OAuth service. The settings
DROPBOX_APP_ID and DROPBOX_API_SECRET must be defined with the values
given by Dropbox application registration process.

By default account id and token expiration time are stored in extra_data
field, check OAuthBackend class for details on how to extend it.
"""
from django.utils import simplejson

from social.backends.oauth import ConsumerBasedOAuth


class DropboxOAuth(ConsumerBasedOAuth):
    """Dropbox OAuth authentication backend"""
    name = 'dropbox'
    ID_KEY = 'uid'
    AUTHORIZATION_URL = 'https://www.dropbox.com/1/oauth/authorize'
    REQUEST_TOKEN_URL = 'https://api.dropbox.com/1/oauth/request_token'
    ACCESS_TOKEN_URL = 'https://api.dropbox.com/1/oauth/access_token'
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from Dropbox account"""
        return {'username': str(response.get('uid')),
                'email': response.get('email'),
                'first_name': response.get('display_name')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://api.dropbox.com/1/account/info'
        request = self.oauth_request(access_token, url)
        response = self.fetch_response(request)
        try:
            return simplejson.loads(response)
        except ValueError:
            return None
