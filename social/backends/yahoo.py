"""
Yahoo OpenId, OAuth2 backends, docs at:
    http://psa.matiasaguirre.net/docs/backends/yahoo.html
"""
from requests import HTTPError
from requests.auth import HTTPBasicAuth

from social.backends.open_id import OpenIdAuth
from social.backends.oauth import BaseOAuth2
from social.exceptions import AuthCanceled, AuthUnknownError


class YahooOpenId(OpenIdAuth):
    """Yahoo OpenID authentication backend"""
    name = 'yahoo'
    URL = 'http://me.yahoo.com'


class YahooOAuth2(BaseOAuth2):
    """Yahoo OAuth2 authentication backend"""
    name = 'yahoo-oauth2'
    ID_KEY = 'guid'
    AUTHORIZATION_URL = 'https://api.login.yahoo.com/oauth2/request_auth'
    ACCESS_TOKEN_URL = 'https://api.login.yahoo.com/oauth2/get_token'
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('xoauth_yahoo_guid', 'id'),
        ('access_token', 'access_token'),
        ('expires_in', 'expires'),
        ('refresh_token', 'refresh_token'),
        ('token_type', 'token_type'),
    ]

    def get_user_names(self, first_name, last_name):
        if first_name or last_name:
            return " ".join((first_name, last_name)), first_name, last_name
        return None, None, None

    def get_user_details(self, response):
        """Return user details from Yahoo Profile"""
        fullname, first_name, last_name = self.get_user_names(
            first_name=response.get('givenName'),
            last_name=response.get('familyName')
        )
        emails = [email for email in response.get('emails', [])
                        if email.get('handle')]
        emails.sort(key=lambda e: e.get('primary', False), reverse=True)
        return {'username': response.get('nickname'),
                'email': emails[0]['handle'] if emails else response.get('guid', ''),
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://social.yahooapis.com/v1/user/{0}/profile?format=json'.format(
                kwargs['response']['xoauth_yahoo_guid'])
        return self.get_json(url, headers={'Authorization': 'Bearer {0}'.format(
            access_token)}, method='GET')['profile']

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        self.process_error(self.data)
        client_id, client_secret = self.get_key_and_secret()
        try:
            response = self.request_access_token(
                self.ACCESS_TOKEN_URL,
                auth=HTTPBasicAuth(client_id, client_secret),
                data=self.auth_complete_params(self.validate_state()),
                headers=self.auth_headers(),
                method=self.ACCESS_TOKEN_METHOD
            )
        except HTTPError as err:
            if err.response.status_code == 400:
                raise AuthCanceled(self)
            else:
                raise
        except KeyError:
            raise AuthUnknownError(self)
        self.process_error(response)
        return self.do_auth(response['access_token'], response=response,
                            *args, **kwargs)

    def auth_complete_params(self, state=None):
        return {
            'grant_type': 'authorization_code',  # request auth code
            'code': self.data.get('code', ''),  # server response code
            'redirect_uri': self.get_redirect_uri(state)
        }
