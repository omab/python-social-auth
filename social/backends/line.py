# vim:fileencoding=utf-8
import requests
import json

from social.backends.oauth import BaseOAuth2
from social.exceptions import AuthFailed
from social.utils import handle_http_errors


class LineOAuth2(BaseOAuth2):
    name = 'line'
    AUTHORIZATION_URL = 'https://access.line.me/dialog/oauth/weblogin'
    ACCESS_TOKEN_URL = 'https://api.line.me/v1/oauth/accessToken'
    BASE_API_URL = 'https://api.line.me'
    USER_INFO_URL = BASE_API_URL + '/v1/profile'
    ACCESS_TOKEN_METHOD = 'POST'
    STATE_PARAMETER = True
    REDIRECT_STATE = True
    ID_KEY = 'mid'
    EXTRA_DATA = [
        ('mid', 'id'),
        ('expire', 'expire'),
        ('refreshToken', 'refresh_token')
    ]

    def auth_params(self, state=None):
        client_id, client_secret = self.get_key_and_secret()
        return {
            'client_id': client_id,
            'redirect_uri': self.get_redirect_uri(),
            'response_type': self.RESPONSE_TYPE
        }

    def process_error(self, data):
        error_code = data.get('errorCode') or \
                     data.get('statusCode') or \
                     data.get('error')
        error_message = data.get('errorMessage') or \
                        data.get('statusMessage') or \
                        data.get('error_desciption')
        if error_code is not None or error_message is not None:
            raise AuthFailed(self, error_message or error_code)

    @handle_http_errors
    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""
        client_id, client_secret = self.get_key_and_secret()
        code = self.data.get('code')

        self.process_error(self.data)

        try:
            response = self.request_access_token(
                self.access_token_url(),
                method=self.ACCESS_TOKEN_METHOD,
                params={
                    'requestToken': code,
                    'channelSecret': client_secret
                }
            )
            self.process_error(response)

            return self.do_auth(response['accessToken'], response=response,
                                *args, **kwargs)
        except requests.HTTPError as err:
            self.process_error(json.loads(err.response.content))

    def get_user_details(self, response):
        response.update({
            'fullname': response.get('displayName'),
            'picture_url': response.get('pictureUrl')
        })
        return response

    def get_user_id(self, details, response):
        """Return a unique ID for the current user, by default from server response."""
        return response.get(self.ID_KEY)

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        try:
            response = self.get_json(
                self.USER_INFO_URL,
                headers={
                    "Authorization": "Bearer {}".format(access_token)
                }
            )
            self.process_error(response)
            return response
        except requests.HTTPError as err:
            self.process_error(err.response.json())
