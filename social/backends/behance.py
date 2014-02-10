"""
Behance OAuth2 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/behance.html
"""
from social.backends.oauth import BaseOAuth2


class BehanceOAuth2(BaseOAuth2):
    """Behance OAuth authentication backend"""
    name = 'behance'
    AUTHORIZATION_URL = 'https://www.behance.net/v2/oauth/authenticate'
    ACCESS_TOKEN_URL = 'https://www.behance.net/v2/oauth/token'
    ACCESS_TOKEN_METHOD = 'POST'
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
