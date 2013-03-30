"""
Dailymotion OAuth2 support.

This adds support for Dailymotion OAuth service. An application must
be registered first on dailymotion and the settings DAILYMOTION_CONSUMER_KEY
and DAILYMOTION_CONSUMER_SECRET must be defined with the corresponding
values.

User screen name is used to generate username.

By default account id is stored in extra_data field, check OAuthBackend
class for details on how to extend it.
"""
from social.backends.oauth import BaseOAuth2


class DailymotionOAuth2(BaseOAuth2):
    """Dailymotion OAuth authentication backend"""
    name = 'dailymotion'
    EXTRA_DATA = [('id', 'id')]
    ID_KEY = 'username'
    AUTHORIZATION_URL = 'https://api.dailymotion.com/oauth/authorize'
    REQUEST_TOKEN_URL = 'https://api.dailymotion.com/oauth/token'
    ACCESS_TOKEN_URL = 'https://api.dailymotion.com/oauth/token'
    ACCESS_TOKEN_METHOD = 'POST'

    def get_user_details(self, response):
        return {'username': response.get('screenname')}

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        return self.get_json('https://api.dailymotion.com/me/',
                             params={'access_token': access_token})

    def oauth_request(self, token, url, extra_params=None):
        return extra_params or {}
