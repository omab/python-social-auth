"""
Mail.ru OAuth2 support

Take a look to http://api.mail.ru/docs/guides/oauth/

You need to register OAuth site here:
http://api.mail.ru/sites/my/add

Then update your settings values using registration information

"""

import json

from urllib import urlencode, unquote
from urllib2 import Request, HTTPError
from hashlib import md5

from social.exceptions import AuthCanceled
from social.backends.oauth import BaseOAuth2


class MailruOAuth2(BaseOAuth2):
    """Mail.ru authentication backend"""
    name = 'mailru-oauth2'
    ID_KEY = 'uid'
    AUTHORIZATION_URL = 'https://connect.mail.ru/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://connect.mail.ru/oauth/token'
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
        except HTTPError:  # Mail.ru returns HTTPError 400 if cancelled
            raise AuthCanceled(self)

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Mail.ru REST API"""
        data = {'method': 'users.getInfo', 'session_key': access_token}
        return mailru_api(self, data)[0]


def mailru_sig(data, secret):
    """ Calculates signature of request data """
    param_list = sorted(list(item + '=' + data[item] for item in data))
    return md5(''.join(param_list) + secret).hexdigest()


def mailru_api(backend, data):
    """Calls Mail.ru REST API http://api.mail.ru/docs/guides/restapi/"""
    key, secret = backend.get_key_and_secret()
    data.update({'app_id': key, 'secure': '1'})
    data['sig'] = mailru_sig(secret, data)
    params = urlencode(data)
    request = Request('http://www.appsmail.ru/platform/api', params)
    try:
        return json.loads(backend.urlopen(request).read())
    except (TypeError, KeyError, IOError, ValueError, IndexError):
        return None
