"""
Vend  OAuth2 backend:

"""
from requests import HTTPError
from social.backends.oauth import BaseOAuth2
from social.exceptions import AuthCanceled, AuthUnknownError


class VendOAuth2(BaseOAuth2):
    name = 'vend'
    AUTHORIZATION_URL = 'https://secure.vendhq.com/connect'
    ACCESS_TOKEN_URL = ''
    SCOPE_SEPARATOR = ' '
    REDIRECT_STATE = False
    REDIRECT_URI_PARAMETER_NAME = 'redirect_uri'
    EXTRA_DATA = [
                     ('refresh_token', 'refresh_token'),
                     ('domain_prefix','domain_prefix')
    ]
    def get_user_id(self, details, response):
        return None
    def get_user_details(self, response):
        return {}

    def user_data(self, access_token, *args, **kwargs):

        return None


    def access_token_url(self):
        return self.ACCESS_TOKEN_URL




    def process_error(self, data):
        error = data.get('error')
        if error:
            if error == 'access_denied':
                raise AuthCanceled(self)
            else:
                raise AuthUnknownError(self, 'Vend error was {0}'.format(
                    error
                ))
        return super(VendOAuth2, self).process_error(data)

    def auth_complete_params(self, state=None):
        client_id, client_secret = self.get_key_and_secret()
        return {
           'code': self.data.get('code', '').encode('ascii', 'ignore'),  # server response code
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'authorization_code',  # request auth code
            'redirect_uri': self.get_redirect_uri(state)
        }

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""

        #Handle dynamic login access_token_url
        self.ACCESS_TOKEN_URL = 'https://{0}.vendhq.com/api/1.0/token'.format(self.data["domain_prefix"])

        self.process_error(self.data)
        try:
            response = self.request_access_token(
                self.ACCESS_TOKEN_URL,
                params=self.auth_complete_params(self.validate_state()),
                headers=self.auth_headers(),
                method='POST',

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
