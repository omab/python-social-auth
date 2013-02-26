"""
Behance OAuth2 support.

This contribution adds support for the Behance OAuth service. The settings
BEHANCE_CLIENT_ID and BEHANCE_CLIENT_SECRET must be defined with the values
given by Behance application registration process.

Extended permissions are supported by defining BEHANCE_EXTENDED_PERMISSIONS
setting, it must be a list of values to request.

By default username and access_token are stored in extra_data field.
"""
from social.backends.oauth import BaseOAuth2


class BehanceOAuth2(BaseOAuth2):
    """Behance OAuth authentication backend"""
    name = 'behance'
    AUTHORIZATION_URL = 'https://www.behance.net/v2/oauth/authenticate'
    ACCESS_TOKEN_URL = 'https://www.behance.net/v2/oauth/token'
    SCOPE_SEPARATOR = '|'
    EXTRA_DATA = [('username', 'username')]
    REDIRECT_STATE = False

    def get_user_id(self, details, response):
        return response['user']['id']

    def get_user_details(self, response):
        """Return user details from Behance account"""
        user = response['user']
        return {'username': user['username'],
                'last_name': user['last_name'],
                'first_name': user['first_name'],
                'fullname': user['display_name'],
                'email': ''}

    def extra_data(self, user, uid, response, details):
        # Pull up the embedded user attributes so they can be found as extra
        # data. See the example token response for possible attributes:
        # http://www.behance.net/dev/authentication#step-by-step
        data = response.copy()
        data.update(response['user'])
        return super(BehanceOAuth2, self).extra_data(user, uid, data, details)
