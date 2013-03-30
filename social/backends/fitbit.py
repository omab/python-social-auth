"""
Fitbit OAuth support.

This contribution adds support for Fitbit OAuth service. The settings
FITBIT_CONSUMER_KEY and FITBIT_CONSUMER_SECRET must be defined with the values
given by Fitbit application registration process.

By default account id, username and token expiration time are stored in
extra_data field, check OAuthBackend class for details on how to extend it.
"""
from social.backends.oauth import BaseOAuth1


class FitbitOAuth(BaseOAuth1):
    """Fitbit OAuth authentication backend"""
    name = 'fitbit'
    AUTHORIZATION_URL = 'https://api.fitbit.com/oauth/authorize'
    REQUEST_TOKEN_URL = 'https://api.fitbit.com/oauth/request_token'
    ACCESS_TOKEN_URL = 'https://api.fitbit.com/oauth/access_token'
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
