"""
Douban OAuth support.

This adds support for Douban OAuth service. An application must
be registered first on douban.com and the settings DOUBAN_CONSUMER_KEY
and DOUBAN_CONSUMER_SECRET must be defined with they corresponding
values.

By default account id is stored in extra_data field, check OAuthBackend
class for details on how to extend it.
"""
from social.backends.oauth import BaseOAuth2, BaseOAuth1


class DoubanOAuth(BaseOAuth1):
    """Douban OAuth authentication backend"""
    name = 'douban'
    EXTRA_DATA = [('id', 'id')]
    AUTHORIZATION_URL = 'http://www.douban.com/service/auth/authorize'
    REQUEST_TOKEN_URL = 'http://www.douban.com/service/auth/request_token'
    ACCESS_TOKEN_URL = 'http://www.douban.com/service/auth/access_token'

    def get_user_id(self, details, response):
        return response['db:uid']['$t']

    def get_user_details(self, response):
        """Return user details from Douban"""
        return {'username': response["db:uid"]["$t"],
                'email': ''}

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        return self.get_json('http://api.douban.com/people/%40me?&alt=json',
                             auth=self.oauth_auth(access_token))


class DoubanOAuth2(BaseOAuth2):
    """Douban OAuth authentication backend"""
    name = 'douban-oauth2'
    AUTHORIZATION_URL = 'https://www.douban.com/service/auth2/auth'
    ACCESS_TOKEN_URL = 'https://www.douban.com/service/auth2/token'
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('id', 'id'),
        ('uid', 'username'),
        ('refresh_token', 'refresh_token'),
    ]

    def get_user_details(self, response):
        """Return user details from Douban"""
        return {'username': response.get('uid', ''),
                'fullname': response.get('name', ''),
                'email': ''}

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        return self.get_json(
            'https://api.douban.com/v2/user/~me',
            headers={'Authorization': 'Bearer {0}'.format(access_token)}
        )
