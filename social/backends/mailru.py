"""
Mail.ru OAuth2 support

Take a look to http://api.mail.ru/docs/guides/oauth/

You need to register OAuth site here:
http://api.mail.ru/sites/my/add

Then update your settings values using registration information

"""
from hashlib import md5

from requests import HTTPError

from social.p3 import unquote
from social.exceptions import AuthCanceled
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
        values = {
            'username': unquote(response['nick']),
            'email': unquote(response['email']),
            'first_name': unquote(response['first_name']),
            'last_name': unquote(response['last_name'])
        }

        if values['first_name'] and values['last_name']:
            values['fullname'] = '%s %s' % (values['first_name'],
                                            values['last_name'])
        return values

    def auth_complete(self, *args, **kwargs):
        try:
            return super(MailruOAuth2, self).auth_complete(*args, **kwargs)
        except HTTPError as err:  # Mail.ru returns HTTPError 400 if cancelled
            if err.response.status_code == 400:
                raise AuthCanceled(self)
            else:
                raise

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Mail.ru REST API"""
        key, secret = self.get_key_and_secret()
        data = {
            'method': 'users.getInfo',
            'session_key': access_token,
            'app_id': key,
            'secure': '1'
        }
        param_list = sorted(list(item + '=' + data[item] for item in data))
        data['sig'] = md5(''.join(param_list) + secret).hexdigest()
        try:
            out = self.get_json('http://www.appsmail.ru/platform/api',
                                 params=data)
            print "OUT:", out
            return out
        except (TypeError, KeyError, IOError, ValueError, IndexError):
            return None
