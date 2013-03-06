# -*- coding: utf-8 -*-
"""
VKontakte OpenAPI and OAuth 2.0 support.

This contribution adds support for VKontakte OpenAPI and OAuth 2.0 service in
the form www.vkontakte.ru. Username is retrieved from the identity returned by
server.
"""
from time import time
from hashlib import md5

from social.backends.base import BaseAuth
from social.backends.oauth import BaseOAuth2
from social.exceptions import AuthTokenRevoked, AuthException


class VKontakteOpenAPI(BaseAuth):
    """VKontakte OpenAPI authentication backend"""
    name = 'vkontakte'
    ID_KEY = 'id'

    def get_user_details(self, response):
        """Return user details from VKontakte request"""
        nickname = response.get('nickname') or ''
        return {
            'username': response['id'] if len(nickname) == 0 else nickname,
            'email': '',
            'fullname': '',
            'first_name': response.get('first_name')[0]
                                if 'first_name' in response else '',
            'last_name': response.get('last_name')[0]
                                if 'last_name' in response else ''
        }

    def user_data(self, access_token, *args, **kwargs):
        return self.data

    def auth_html(self):
        """Returns local VK authentication page, not necessary for
        VK to authenticate.
        """
        ctx = {'VK_APP_ID': self.setting('APP_ID'),
               'VK_COMPLETE_URL': self.redirect_uri}
        local_html = self.setting('LOCAL_HTML', 'vkontakte.html')
        return self.strategy.render_html(tpl=local_html, context=ctx)

    def auth_complete(self, *args, **kwargs):
        """Performs check of authentication in VKontakte, returns User if
        succeeded"""
        app_cookie = 'vk_app_' + self.setting('APP_ID')

        if not 'id' in self.data or not self.strategy.cookie_get(app_cookie):
            raise ValueError('VKontakte authentication is not completed')

        key, secret = self.get_key_and_secret()
        cookie_dict = dict(item.split('=') for item in
                               self.strategy.cookie_get(app_cookie).split('&'))
        check_str = ''.join(item + '=' + cookie_dict[item]
                                for item in ['expire', 'mid', 'secret', 'sid'])

        hash = md5(check_str + secret).hexdigest()

        if hash != cookie_dict['sig'] or int(cookie_dict['expire']) < time():
            raise ValueError('VKontakte authentication failed: invalid hash')
        else:
            kwargs.update({'backend': self,
                           'response': self.user_data(cookie_dict['mid'])})
            return self.strategy.authenticate(*args, **kwargs)

    def uses_redirect(self):
        """VKontakte does not require visiting server url in order
        to do authentication, so auth_xxx methods are not needed to be called.
        Their current implementation is just an example"""
        return False


class VKontakteOAuth2(BaseOAuth2):
    """VKontakteOAuth2 authentication backend"""
    name = 'vkontakte-oauth2'
    ID_KEY = 'user_id'
    AUTHORIZATION_URL = 'http://oauth.vk.com/authorize'
    ACCESS_TOKEN_URL = 'https://oauth.vk.com/access_token'
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from Vkontakte account"""
        return {'username': response.get('screen_name'),
                'email': '',
                'first_name': response.get('first_name'),
                'last_name': response.get('last_name')}

    def user_data(self, access_token, response, *args, **kwargs):
        """Loads user data from service"""
        request_data = ['first_name', 'last_name', 'screen_name', 'nickname',
                        'photo'] + self.setting('EXTRA_DATA', [])

        fields = ','.join(set(request_data))
        data = vkontakte_api(self, 'users.get', {
            'access_token': access_token,
            'fields': fields,
            'uids': response.get('user_id')
        })

        if data.get('error'):
            error = data['error']
            msg = error.get('error_msg', 'Unknown error')
            if error.get('error_code') == 5:
                raise AuthTokenRevoked(self, msg)
            else:
                raise AuthException(self, msg)

        if data:
            data = data.get('response')[0]
            data['user_photo'] = data.get('photo')  # Backward compatibility
        return data


class VKontakteAppOAuth2(VKontakteOAuth2):
    """VKontakte Application Authentication support"""
    name = 'vkontakte-app'

    def user_profile(self, user_id, access_token=None):
        data = {'uids': user_id, 'fields': 'photo'}
        if access_token:
            data['access_token'] = access_token
        profiles = vkontakte_api(self, 'getProfiles', data).get('response')
        if profiles:
            return profiles[0]

    def auth_complete(self, *args, **kwargs):
        required_params = ('is_app_user', 'viewer_id', 'access_token',
                           'api_id')
        if not all(param in self.data for param in required_params):
            return None

        auth_key = self.data.get('auth_key')

        # Verify signature, if present
        key, secret = self.get_key_and_secret()
        if auth_key:
            check_key = md5('_'.join([self.data.get('api_id'),
                                      self.data.get('viewer_id'),
                                      key])).hexdigest()
            if check_key != auth_key:
                raise ValueError('VKontakte authentication failed: invalid '
                                 'auth key')

        user_check = self.setting('USERMODE')
        user_id = self.data.get('viewer_id')
        if user_check is not None:
            user_check = int(user_check)
            if user_check == 1:
                is_user = self.data.get('is_app_user')
            elif user_check == 2:
                is_user = vkontakte_api(self, 'isAppUser',
                                        {'uid': user_id}).get('response', 0)
            if not int(is_user):
                return None
        return self.strategy.authenticate(*args, **{'auth': self,
            'backend': self,
            'request': self.request,
            'response': {
                'response': self.user_profile(user_id),
                'user_id': user_id,
            }
        })


def vkontakte_api(backend, method, data):
    """Calls VKontakte OpenAPI method
        http://vkontakte.ru/apiclub,
        http://vkontakte.ru/pages.php?o=-1&p=%C2%FB%EF%EE%EB%ED%E5%ED%E8%E5%20
                                             %E7%E0%EF%F0%EE%F1%EE%E2%20%EA%20
                                             API
    """
    # We need to perform server-side call if no access_token
    if not 'access_token' in data:
        if not 'v' in data:
            data['v'] = '3.0'

        key, secret = backend.get_key_and_secret()
        if not 'api_id' in data:
            data['api_id'] = key

        data['method'] = method
        data['format'] = 'json'
        url = 'http://api.vkontakte.ru/api.php'
        param_list = sorted(list(item + '=' + data[item] for item in data))
        data['sig'] = md5(''.join(param_list) + secret).hexdigest()
    else:
        url = 'https://api.vkontakte.ru/method/' + method

    try:
        return backend.get_json(url, params=data)
    except (TypeError, KeyError, IOError, ValueError, IndexError):
        return None
