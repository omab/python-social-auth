#coding:utf8
#author:hepochen@gmail.com  https://github.com/hepochen
"""
Weibo OAuth2 support.

This script adds support for Weibo OAuth service. An application must
be registered first on http://open.weibo.com.

WEIBO_CLIENT_KEY and WEIBO_CLIENT_SECRET must be defined in the settings.py
correctly.

By default account id,profile_image_url,gender are stored in extra_data field,
check OAuthBackend class for details on how to extend it.
"""
from social.backends.oauth import BaseOAuth2


class WeiboOAuth2(BaseOAuth2):
    """Weibo (of sina) OAuth authentication backend"""
    name = 'weibo'
    ID_KEY = 'uid'
    AUTHORIZATION_URL = 'https://api.weibo.com/oauth2/authorize'
    REQUEST_TOKEN_URL = 'https://api.weibo.com/oauth2/request_token'
    ACCESS_TOKEN_URL = 'https://api.weibo.com/oauth2/access_token'
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('id', 'id'),
        ('name', 'username'),
        ('profile_image_url', 'profile_image_url'),
        ('gender', 'gender')
    ]

    def get_user_details(self, response):
        """Return user details from Weibo. API URL is:
        https://api.weibo.com/2/users/show.json/?uid=<UID>&access_token=<TOKEN>
        """
        return {'username': response.get("name", ""),
                'first_name': response.get('screen_name', '')}

    def user_data(self, access_token, *args, **kwargs):
        return self.get_json('https://api.weibo.com/2/users/show.json',
                             params={'access_token': access_token,
                                     'uid': args[0]['uid']})
