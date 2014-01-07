"""
Dropbox OAuth1 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/dropbox.html
"""
from social.backends.oauth import BaseOAuth1, BaseOAuth2


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


class DropboxOAuth2(BaseOAuth2):
    name = 'dropbox-oauth2'
    ID_KEY = 'uid'
    AUTHORIZATION_URL = 'https://www.dropbox.com/1/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://api.dropbox.com/1/oauth2/token'
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('uid', 'username'),
    ]

    def get_user_details(self, response):
        """Return user details from Dropbox account"""
        return {'username': str(response.get('uid')),
                'email': response.get('email'),
                'first_name': response.get('display_name')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json(
            'https://api.dropbox.com/1/account/info',
            headers={'Authorization': 'Bearer {0}'.format(access_token)}
        )
