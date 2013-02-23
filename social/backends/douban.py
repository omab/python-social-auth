"""
Douban OAuth support.

This adds support for Douban OAuth service. An application must
be registered first on douban.com and the settings DOUBAN_CONSUMER_KEY
and DOUBAN_CONSUMER_SECRET must be defined with they corresponding
values.

By default account id is stored in extra_data field, check OAuthBackend
class for details on how to extend it.
"""
import json
from urllib2 import Request

from social.backends.oauth import BaseOAuth2, ConsumerBasedOAuth
from social.exceptions import AuthCanceled


class DoubanOAuth(ConsumerBasedOAuth):
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
        url = 'http://api.douban.com/people/%40me?&alt=json'
        request = self.oauth_request(access_token, url)
        data = self.fetch_response(request)
        try:
            return json.loads(data)
        except ValueError:
            return None

    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""
        if 'denied' in self.data:
            raise AuthCanceled(self)
        else:
            return super(DoubanOAuth, self).auth_complete(*args, **kwargs)


class DoubanOAuth2(BaseOAuth2):
    """Douban OAuth authentication backend"""
    name = 'douban2'
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
        url = 'https://api.douban.com/v2/user/~me'
        headers = {'Authorization': 'Bearer %s' % access_token}
        request = Request(url, headers=headers)
        try:
            return json.loads(self.urlopen(request).read())
        except (ValueError, KeyError, IOError):
            return None

    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""
        if 'denied' in self.data:
            raise AuthCanceled(self)
        else:
            return super(DoubanOAuth2, self).auth_complete(*args, **kwargs)


BACKENDS = {
    'douban': DoubanOAuth,
    'douban2': DoubanOAuth2
}
