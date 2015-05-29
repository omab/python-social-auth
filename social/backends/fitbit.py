"""
Fitbit OAuth1 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/fitbit.html
"""
from social.backends.oauth import BaseOAuth1


class FitbitOAuth(BaseOAuth1):
    """Fitbit OAuth authentication backend"""
    name = 'fitbit'
    AUTHORIZATION_URL = 'https://www.fitbit.com/oauth/authorize'
    REQUEST_TOKEN_URL = 'https://api.fitbit.com/oauth/request_token'
    ACCESS_TOKEN_URL = 'https://api.fitbit.com/oauth/access_token'
    ID_KEY = 'encodedId'
    EXTRA_DATA = [('encodedId', 'id'),
                  ('displayName', 'username')]

    def get_user_details(self, response):
        """Return user details from Fitbit account"""
        return {'username': response.get('displayName'),
                'email': ''}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json(
            'https://api.fitbit.com/1/user/-/profile.json',
            auth=self.oauth_auth(access_token)
        )['user']
