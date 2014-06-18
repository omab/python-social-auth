"""
Created on May 13, 2014

@author: Yong Zhang (zyfyfe@gmail.com)
"""

import json

from social.utils import parse_qs
from social.backends.oauth import BaseOAuth2


class QQOAuth2(BaseOAuth2):
    name = 'qq'
    ID_KEY = 'openid'
    AUTHORIZE_URL = 'https://graph.qq.com/oauth2.0/authorize'
    ACCESS_TOKEN_URL = 'https://graph.qq.com/oauth2.0/token'
    AUTHORIZATION_URL = 'https://graph.qq.com/oauth2.0/authorize'
    OPENID_URL = 'https://graph.qq.com/oauth2.0/me'
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('nickname', 'username'),
        ('figureurl_qq_1', 'profile_image_url'),
        ('gender', 'gender')
    ]

    def get_user_details(self, response):
        return {
            'username': response.get('nickname', '')
        }

    def get_openid(self, access_token):
        response = self.request(self.OPENID_URL, params={
            'access_token': access_token
        })
        data = json.loads(response.content[10:-3])
        return data['openid']

    def user_data(self, access_token, *args, **kwargs):
        openid = self.get_openid(access_token)
        response = self.get_json(
            'https://graph.qq.com/user/get_user_info', params={
                'access_token': access_token,
                'oauth_consumer_key': self.setting('SOCIAL_AUTH_QQ_KEY'),
                'openid': openid
            }
        )
        response['openid'] = openid
        return response

    def request_access_token(self, url, data, *args, **kwargs):
        response = self.request(url, params=data, *args, **kwargs)
        return parse_qs(response.content)
