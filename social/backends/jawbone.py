"""
Jawbone OAuth2 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/jawbone.html
"""
from social.backends.oauth import BaseOAuth2
from social.exceptions import AuthCanceled, AuthUnknownError


class JawboneOAuth2(BaseOAuth2):
    name = 'jawbone'
    AUTHORIZATION_URL = 'https://jawbone.com/auth/oauth2/auth'
    ACCESS_TOKEN_URL = 'https://jawbone.com/auth/oauth2/token'
    SCOPE_SEPARATOR = ' '
    REDIRECT_STATE = False

    def get_user_id(self, details, response):
        return response['data']['xid']

    def get_user_details(self, response):
        """Return user details from Jawbone account"""
        data = response['data']
        fullname, first_name, last_name = self.get_user_names(
            first_name=data.get('first', ''),
            last_name=data.get('last', '')
        )
        return {
            'username': first_name + ' ' + last_name,
            'fullname': fullname,
            'first_name': first_name,
            'last_name': last_name,
            'dob': data.get('dob', ''),
            'gender': data.get('gender', ''),
            'height': data.get('height', ''),
            'weight': data.get('weight', '')
        }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json(
            'https://jawbone.com/nudge/api/users/@me',
            headers={'Authorization': 'Bearer ' + access_token},
        )

    def process_error(self, data):
        error = data.get('error')
        if error:
            if error == 'access_denied':
                raise AuthCanceled(self)
            else:
                raise AuthUnknownError(self, 'Jawbone error was {0}'.format(
                    error
                ))
        return super(JawboneOAuth2, self).process_error(data)
