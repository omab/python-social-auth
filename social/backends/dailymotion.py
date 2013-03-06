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
from requests import HTTPError

from social.backends.oauth import BaseOAuth2
from social.exceptions import AuthCanceled


class DailymotionOAuth2(BaseOAuth2):
    """Dailymotion OAuth authentication backend"""
    name = 'dailymotion'
    EXTRA_DATA = [('id', 'id')]
    ID_KEY = 'username'
    AUTHORIZATION_URL = 'https://api.dailymotion.com/oauth/authorize'
    REQUEST_TOKEN_URL = 'https://api.dailymotion.com/oauth/token'
    ACCESS_TOKEN_URL = 'https://api.dailymotion.com/oauth/token'

    def get_user_details(self, response):
        return {'username': response.get('screenname')}

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        try:
            return self.get_json('https://api.dailymotion.com' + access_token)
        except (ValueError, HTTPError):
            return None

    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""
        if 'denied' in self.data:
            raise AuthCanceled(self)
        return super(DailymotionOAuth2, self).auth_complete(*args, **kwargs)

    def oauth_request(self, token, url, extra_params=None):
        return extra_params or {}
