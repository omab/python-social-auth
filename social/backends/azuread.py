"""
Azure AD OAuth2 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/azuread.html
"""
import datetime
from calendar import timegm
from social.exceptions import AuthException, AuthFailed, AuthCanceled, \
                              AuthUnknownError, AuthMissingParameter, \
                              AuthTokenError
from jwt import DecodeError, ExpiredSignature, decode as jwt_decode
from social.backends.oauth import BaseOAuth2
import urllib

class AzureADOAuth2(BaseOAuth2):
    name = 'azuread-oauth2'
    SCOPE_SEPARATOR = ' '
    AUTHORIZATION_URL = 'https://login.windows.net/common/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://login.windows.net/common/oauth2/token'
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False
    DEFAULT_SCOPE = ['openid', 'profile', 'user_impersonation']
    EXTRA_DATA = [
        ('access_token', 'access_token'),
        ('id_token', 'id_token'),
        ('refresh_token', 'refresh_token'),
        ('expires_in', 'expires'),
        ('given_name', 'first_name'),
        ('family_name', 'last_name'),
        ('token_type', 'token_type')
    ]

    def get_user_id(self, details, response):
        """Use upn as unique id"""
        return response.get('upn')

    def get_user_details(self, response):
        """Return user details from Azure AD account"""
        fullname, first_name, last_name = (
            response.get('name', ''),
            response.get('given_name', ''),
            response.get('family_name', '')
        )
        return {'username': fullname,
                'email': response.get('upn'),
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        response = kwargs.get('response')
        id_token = response.get('id_token')
        
        try:
            decoded_id_token = jwt_decode(id_token, verify=False)
        except (DecodeError, ExpiredSignature) as de:
            raise AuthTokenError(self, de)
        
        return decoded_id_token

    def auth_extra_arguments(self):
        """Return extra arguments needed on auth process. The defaults can be
        overriden by GET parameters."""
        extra_arguments = {}
        resource = self.setting('RESOURCE')
        
        if resource:
            extra_arguments = {
                'resource': resource
            }
        
        return extra_arguments

    def extra_data(self, user, uid, response, details=None):
        """Return access_token and extra defined names to store in
        extra_data field"""
        data = super(BaseOAuth2, self).extra_data(user, uid, response, details)
        data['resource'] = self.setting('RESOURCE')
        return data
