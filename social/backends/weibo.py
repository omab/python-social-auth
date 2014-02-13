#coding:utf8
# author:hepochen@gmail.com  https://github.com/hepochen
"""
Weibo OAuth2 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/weibo.html
"""
from social.backends.oauth import BaseOAuth2


class WeiboOAuth2(BaseOAuth2):
    """Weibo (of sina) OAuth authentication backend"""
    name = 'weibo'
    ID_KEY = 'uid'
    AUTHORIZATION_URL = 'https://api.weibo.com/oauth2/authorize'
    REQUEST_TOKEN_URL = 'https://api.weibo.com/oauth2/request_token'
    ACCESS_TOKEN_URL = 'https://api.weibo.com/oauth2/access_token'
    ACCESS_TOKEN_METHOD = 'POST'
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
        if self.setting('DOMAIN_AS_USERNAME'):
            username = response.get('domain', '')
        else:
            username = response.get('name', '')
        return {'username': username,
                'first_name': response.get('screen_name', '')}

    def user_data(self, access_token, *args, **kwargs):
        return self.get_json('https://api.weibo.com/2/users/show.json',
                             params={'access_token': access_token,
                                     'uid': kwargs['response']['uid']})
