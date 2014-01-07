import urllib2,urllib
from urllib2 import Request, urlopen, HTTPError
from urllib import urlencode
from urlparse import urlsplit
import json
from social.exceptions import AuthFailed
from social.backends.oauth import BaseOAuth2
# taobao OAuth base configuration
TAOBAO_OAUTH_HOST = 'oauth.taobao.com'
# TAOBAO_OAUTH_ROOT = 'authorize'
#Always use secure connection
TAOBAO_OAUTH_AUTHORIZATION_URL = 'https://%s/authorize' % (TAOBAO_OAUTH_HOST)
TAOBAO_OAUTH_ACCESS_TOKEN_URL = 'https://%s/token' % (TAOBAO_OAUTH_HOST)

TAOBAO_CHECK_AUTH = 'https://eco.taobao.com/router/rest'
        
class TAOBAOAuth(BaseOAuth2):
    """Taobao OAuth authentication mechanism"""
    name="taobao"
    ID_KEY='taobao_user_id'
    AUTHORIZATION_URL = TAOBAO_OAUTH_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = TAOBAO_OAUTH_ACCESS_TOKEN_URL
   
    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        params = {'method':'taobao.user.get',
                  'fomate':'json',
                  'v':'2.0',
                  'access_token': access_token}
        try:
            return self.get_json(TAOBAO_CHECK_AUTH, params=params)
        except ValueError:
            return None

    def get_user_details(self, response):
        """Return user details from Taobao account"""
        username = response.get('taobao_user_nick')
        return {'username': username}

# Backend definition
BACKENDS = {
    'taobao': TAOBAOAuth,
}
