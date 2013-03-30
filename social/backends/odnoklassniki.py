"""
Odnoklassniki.ru OAuth2 and IFRAME application support
If you are using OAuth2 authentication,
    * Take a look to:
        http://dev.odnoklassniki.ru/wiki/display/ok/The+OAuth+2.0+Protocol
    * You need to register OAuth application here:
        http://dev.odnoklassniki.ru/wiki/pages/viewpage.action?pageId=13992188
elif you're building iframe application,
    * Take a look to:
        http://dev.odnoklassniki.ru/wiki/display/ok/
                Odnoklassniki.ru+Third+Party+Platform
    * You need to register your iframe application here:
        http://dev.odnoklassniki.ru/wiki/pages/viewpage.action?pageId=5668937
    * You need to sign a public offer and do some bureaucracy if you want to be
      listed in application registry
Then setup your application according manual and use information from
registration mail to set settings values.
"""
from hashlib import md5

from social.p3 import unquote
from social.backends.base import BaseAuth
from social.backends.oauth import BaseOAuth2
from social.exceptions import AuthFailed


class OdnoklassnikiOAuth2(BaseOAuth2):
    """Odnoklassniki authentication backend"""
    name = 'odnoklassniki-oauth2'
    ID_KEY = 'uid'
    AUTHORIZATION_URL = 'http://www.odnoklassniki.ru/oauth/authorize'
    ACCESS_TOKEN_URL = 'http://api.odnoklassniki.ru/oauth/token.do'
    EXTRA_DATA = [('refresh_token', 'refresh_token'),
                  ('expires_in', 'expires')]

    def get_user_details(self, response):
        """Return user details from Odnoklassniki request"""
        return {
            'username': response['uid'],
            'email': '',
            'fullname': unquote(response['name']),
            'first_name': unquote(response['first_name']),
            'last_name': unquote(response['last_name'])
        }

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Odnoklassniki REST API"""
        data = {'access_token': access_token, 'method': 'users.getCurrentUser'}
        key, secret = self.get_key_and_secret()
        public_key = self.setting('PUBLIC_NAME')
        return odnoklassniki_api(self, data, 'http://api.odnoklassniki.ru/',
                                 public_key, secret, 'oauth')


class OdnoklassnikiApp(BaseAuth):
    """Odnoklassniki iframe app authentication backend"""
    name = 'odnoklassniki-app'
    ID_KEY = 'uid'

    def extra_data(self, user, uid, response, details):
        return dict([(key, value) for key, value in response.items()
                            if key in response['extra_data_list']])

    def get_user_details(self, response):
        return {
            'username': response['uid'],
            'email': '',
            'fullname': unquote(response['name']),
            'first_name': unquote(response['first_name']),
            'last_name': unquote(response['last_name'])
        }

    def auth_complete(self, request, user, *args, **kwargs):
        self.verify_auth_sig()
        response = self.get_response()
        fields = ('uid', 'first_name', 'last_name', 'name') + \
                 self.setting('EXTRA_USER_DATA_LIST', ())
        data = {
            'method': 'users.getInfo',
            'uids': '{0}'.format(response['logged_user_id']),
            'fields': ','.join(fields),
        }
        client_key, client_secret = self.get_key_and_secret()
        public_key = self.setting('PUBLIC_NAME')
        details = odnoklassniki_api(self, data, response['api_server'],
                                    public_key, client_secret,
                                    'iframe_nosession')
        if len(details) == 1 and 'uid' in details[0]:
            details = details[0]
            auth_data_fields = self.setting('EXTRA_AUTH_DATA_LIST',
                                            ('api_server', 'apiconnection',
                                             'session_key', 'authorized',
                                             'session_secret_key'))

            for field in auth_data_fields:
                details[field] = response[field]
            details['extra_data_list'] = fields + auth_data_fields
            kwargs.update({'backend': self, 'response': details})
        else:
            raise AuthFailed('Cannot get user details: API error')
        return self.strategy.authenticate(*args, **kwargs)

    def get_auth_sig(self):
        secret_key = self.setting('APP_SECRET')
        hash_source = '{0:d}{1:s}{2:s}'.format(self.data['logged_user_id'],
                                               self.data['session_key'],
                                               secret_key)
        return md5(hash_source).hexdigest()

    def get_response(self):
        fields = ('logged_user_id', 'api_server', 'application_key',
                  'session_key', 'session_secret_key', 'authorized',
                  'apiconnection')
        return dict((name, self.data[name]) for name in fields
                        if name in self.data)

    def verify_auth_sig(self):
        correct_key = self.get_auth_sig()
        key = self.data['auth_sig'].lower()
        if correct_key != key:
            raise AuthFailed(self, 'Wrong authorization key')


def odnoklassniki_oauth_sig(data, client_secret):
    """
    Calculates signature of request data access_token value must be included
    Algorithm is described at
        http://dev.odnoklassniki.ru/wiki/pages/viewpage.action?pageId=12878032,
    search for "little bit different way"
    """
    suffix = md5('{0:s}{1:s}'.format(data['access_token'],
                                     client_secret)).hexdigest()
    check_list = sorted(['{0:s}={1:s}'.format(key, value)
                            for key, value in data.items()
                                if key != 'access_token'])
    return md5(''.join(check_list) + suffix).hexdigest()


def odnoklassniki_iframe_sig(data, client_secret_or_session_secret):
    """
    Calculates signature as described at:
        http://dev.odnoklassniki.ru/wiki/display/ok/
            Authentication+and+Authorization
    If API method requires session context, request is signed with session
    secret key. Otherwise it is signed with application secret key
    """
    param_list = sorted(['{0:s}={1:s}'.format(key, value)
                            for key, value in data.items()])
    return md5(''.join(param_list) +
               client_secret_or_session_secret).hexdigest()


def odnoklassniki_api(backend, data, api_url, public_key, client_secret,
                      request_type='oauth'):
    """Calls Odnoklassniki REST API method
    http://dev.odnoklassniki.ru/wiki/display/ok/Odnoklassniki+Rest+API"""
    data.update({
        'application_key': public_key,
        'format': 'JSON'
    })
    if request_type == 'oauth':
        data['sig'] = odnoklassniki_oauth_sig(data, client_secret)
    elif request_type == 'iframe_session':
        data['sig'] = odnoklassniki_iframe_sig(data,
                                               data['session_secret_key'])
    elif request_type == 'iframe_nosession':
        data['sig'] = odnoklassniki_iframe_sig(data, client_secret)
    else:
        msg = 'Unknown request type {0}. How should it be signed?'
        raise AuthFailed(backend, msg.format(request_type))
    return backend.get_json(api_url + 'fb.do', params=data)
