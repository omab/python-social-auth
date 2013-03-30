"""
Stackoverflow OAuth support.

This contribution adds support for Stackoverflow OAuth service. The settings
SOCIAL_AUTH_STACKOVERFLOW_KEY, SOCIAL_AUTH_STACKOVERFLOW_SECRET and
SOCIAL_AUTH_STACKOVERFLOW_API_KEY must be defined with the values given by
Stackoverflow application registration process.

Extended permissions are supported by defining SOCIAL_AUTH_STACKOVERFLOW_SCOPE
setting, it must be a list of values to request.

By default account id and token expiration time are stored in extra_data
field, check OAuthBackend class for details on how to extend it.
"""
from social.backends.oauth import BaseOAuth2


class StackoverflowOAuth2(BaseOAuth2):
    """Stackoverflow OAuth2 authentication backend"""
    name = 'stackoverflow'
    ID_KEY = 'user_id'
    AUTHORIZATION_URL = 'https://stackexchange.com/oauth'
    ACCESS_TOKEN_URL = 'https://stackexchange.com/oauth/access_token'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from Stackoverflow account"""
        return {'username': response.get('link').rsplit('/', 1)[-1],
                'full_name': response.get('display_name')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json('https://api.stackexchange.com/2.1/me',
                             params={'site': 'stackoverflow',
                                     'access_token': access_token,
                                     'key': self.setting('API_KEY')}
        )['items'][0]

    def request_access_token(self, *args, **kwargs):
        return self.get_querystring(*args, **kwargs)
