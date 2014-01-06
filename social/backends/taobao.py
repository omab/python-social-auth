import urllib2,urllib
from urllib2 import Request, urlopen, HTTPError
from urllib import urlencode
from urlparse import urlsplit
from social_auth.backends.exceptions import StopPipeline, AuthException, \
                                            AuthFailed, AuthCanceled, \
                                            AuthUnknownError, AuthTokenError, \
                                            AuthMissingParameter
from django.conf import settings
from django.utils import simplejson
import json
from django.contrib.auth import authenticate
from social_auth.backends import BaseOAuth2, OAuthBackend, USERNAME
# taobao OAuth base configuration
TAOBAO_OAUTH_HOST = 'oauth.taobao.com'
# TAOBAO_OAUTH_ROOT = 'authorize'
#Always use secure connection
TAOBAO_OAUTH_REQUEST_TOKEN_URL = 'https://%s/request_token' % (TAOBAO_OAUTH_HOST)
TAOBAO_OAUTH_AUTHORIZATION_URL = 'https://%s/authorize' % (TAOBAO_OAUTH_HOST)
TAOBAO_OAUTH_ACCESS_TOKEN_URL = 'https://%s/token' % (TAOBAO_OAUTH_HOST)

TAOBAO_CHECK_AUTH = 'https://eco.taobao.com/router/rest'
TAOBAO_USER_SHOW = 'https://%s/user/get_user_info' % TAOBAO_OAUTH_HOST
class TAOBAOBackend(OAuthBackend):
    """Taobao OAuth authentication backend"""
    name = 'taobao'

    def get_user_id(self, details, response):
        return response['taobao_user_id']
    
    def get_user_details(self, response):
        """Return user details from Taobao account"""
        
        username = response['taobao_user_nick']
        return {USERNAME: username,
                'email': '',  # not supplied
                'last_name': ''}
        
class TAOBAOAuth(BaseOAuth2):
    """Taobao OAuth authentication mechanism"""
    AUTHORIZATION_URL = TAOBAO_OAUTH_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = TAOBAO_OAUTH_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = TAOBAO_OAUTH_ACCESS_TOKEN_URL
    SERVER_URL = TAOBAO_OAUTH_HOST
    AUTH_BACKEND = TAOBAOBackend
    SETTINGS_KEY_NAME = 'TAOBAO_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'TAOBAO_CONSUMER_SECRET'
   
    def user_data(self, access_token):
        """Return user data provided"""
        params = {'method':'taobao.user.get',
                  'fomate':'json',
                  'v':'2.0',
                  'access_token': access_token}
        
        url = TAOBAO_CHECK_AUTH + urllib.urlencode(params)
        # # print url
       
        try:
            return simplejson.load(urllib.urlopen(url))
        except ValueError:
            return None

# Backend definition
BACKENDS = {
    'taobao': TAOBAOAuth,
}
