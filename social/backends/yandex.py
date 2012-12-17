"""
Yandex OpenID and OAuth2 support.

This contribution adds support for Yandex.ru OpenID service in the form
openid.yandex.ru/user. Username is retrieved from the identity url.

If username is not specified, OpenID 2.0 url used for authentication.
"""
import json
from urllib import urlencode
from urlparse import urlparse, urlsplit

from social.backends.open_id import OpenIdAuth
from social.backends.oauth import BaseOAuth2, OAuthAuth


# Yandex configuration
YANDEX_AUTHORIZATION_URL = 'https://oauth.yandex.ru/authorize'
YANDEX_ACCESS_TOKEN_URL = 'https://oauth.yandex.ru/token'
YANDEX_SERVER = 'oauth.yandex.ru'


class YandexOpenId(OpenIdAuth):
    """Yandex OpenID authentication backend"""
    name = 'yandex'

    def get_user_id(self, details, response):
        return details['email'] or response.identity_url

    def get_user_details(self, response):
        """Generate username from identity url"""
        values = super(YandexOpenId, self).get_user_details(response)
        values['username'] = values.get('username') or\
                             urlsplit(response.identity_url)\
                                    .path.strip('/')
        values['email'] = values.get('email', '')
        return values

    def openid_url(self):
        """Returns Yandex authentication URL"""
        return 'http://openid.yandex.ru'


class YandexOAuth(OAuthAuth):
    """Yandex OAuth authentication backend"""
    name = 'yaru'
    AUTHORIZATION_URL = YANDEX_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = YANDEX_ACCESS_TOKEN_URL
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        return get_user_details(response)

    def user_data(self, access_token, response, *args, **kwargs):
        url = 'https://api-yaru.yandex.ru/me/'
        return user_data(self, url, access_token, response, *args, **kwargs)


class YandexOAuth2(BaseOAuth2):
    """Legacy Yandex OAuth2 authentication backend"""
    name = 'yandex-oauth2'

    def get_user_details(self, response):
        return get_user_details(response)

    def user_data(self, access_token, response, *args, **kwargs):
        url = self.strategy.setting('API_URL')
        reply = user_data(self, url, access_token, response, *args, **kwargs)
        if reply:
            if isinstance(reply, list) and len(reply) >= 1:
                reply = reply[0]
            if 'links' in reply:
                userpic = reply['links'].get('avatar')
            elif 'avatar' in reply:
                userpic = reply['avatar'].get('Portrait')
            else:
                userpic = ''
            reply.update({'id': reply['id'].split("/")[-1],
                          'access_token': access_token,
                          'userpic': userpic})
        return reply


def get_user_details(response):
    """Return user details from Yandex account"""
    name = response['name']
    last_name = ''

    if ' ' in name:
        names = name.split(' ')
        last_name = names[0]
        first_name = names[1]
    else:
        first_name = name

    try:
        host = urlparse(response.get('links').get('www')).hostname
        username = host.split('.')[0]
    except (IndexError, AttributeError):
        username = name.replace(' ', '')

    return {
        'username': username,
        'email':  response.get('email', ''),
        'first_name': first_name,
        'last_name': last_name,
    }


def user_data(backend, url, access_token, response, *args, **kwargs):
    """Loads user data from service"""
    url = url + '?' + urlencode({
        'oauth_token': access_token,
        'format': 'json',
        'text': 1
    })
    try:
        return json.load(backend.urlopen(url))
    except (ValueError, IndexError):
        return None


# Backend definition
BACKENDS = {
    'yandex-openid': YandexOpenId,
    'yandex-oauth': YandexOAuth,
    'yandex-oauth2': YandexOAuth2
}
