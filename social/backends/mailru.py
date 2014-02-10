"""
Mail.ru OAuth2 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/mailru.html
"""
from hashlib import md5

from social.p3 import unquote
from social.backends.oauth import BaseOAuth2


class MailruOAuth2(BaseOAuth2):
    """Mail.ru authentication backend"""
    name = 'mailru-oauth2'
    ID_KEY = 'uid'
    AUTHORIZATION_URL = 'https://connect.mail.ru/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://connect.mail.ru/oauth/token'
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [('refresh_token', 'refresh_token'),
                  ('expires_in', 'expires')]

    def get_user_details(self, response):
        """Return user details from Mail.ru request"""
        values = {'username': unquote(response['nick']),
                  'email': unquote(response['email']),
                  'first_name': unquote(response['first_name']),
                  'last_name': unquote(response['last_name'])}
        if values['first_name'] and values['last_name']:
            values['fullname'] = ' '.join((values['first_name'],
                                           values['last_name']))
        return values

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Mail.ru REST API"""
        key, secret = self.get_key_and_secret()
        data = {'method': 'users.getInfo',
                'session_key': access_token,
                'app_id': key,
                'secure': '1'}
        param_list = sorted(list(item + '=' + data[item] for item in data))
        data['sig'] = md5(
            (''.join(param_list) + secret).encode('utf-8')
        ).hexdigest()
        return self.get_json('http://www.appsmail.ru/platform/api',
                             params=data)[0]
