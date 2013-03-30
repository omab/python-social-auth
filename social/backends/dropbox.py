"""
Dropbox OAuth support.

This contribution adds support for Dropbox OAuth service. The settings
DROPBOX_APP_ID and DROPBOX_API_SECRET must be defined with the values
given by Dropbox application registration process.

By default account id and token expiration time are stored in extra_data
field, check OAuthBackend class for details on how to extend it.
"""
from social.backends.oauth import BaseOAuth1


class DropboxOAuth(BaseOAuth1):
    """Dropbox OAuth authentication backend"""
    name = 'dropbox'
    ID_KEY = 'uid'
    AUTHORIZATION_URL = 'https://www.dropbox.com/1/oauth/authorize'
    REQUEST_TOKEN_URL = 'https://api.dropbox.com/1/oauth/request_token'
    REQUEST_TOKEN_METHOD = 'POST'
    ACCESS_TOKEN_URL = 'https://api.dropbox.com/1/oauth/access_token'
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_URI_PARAMETER_NAME = 'oauth_callback'
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
        return self.get_json('https://api.dropbox.com/1/account/info',
                             auth=self.oauth_auth(access_token))
