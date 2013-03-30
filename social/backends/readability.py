"""
Readability OAuth support.

This contribution adds support for Readability OAuth service. The settings
SOCIAL_AUTH_READABILITY_CONSUMER_KEY and
SOCIAL_AUTH_READABILITY_CONSUMER_SECRET must be defined with the values given
by Readability in the Connections page of your account settings.
"""
from social.backends.oauth import BaseOAuth1


READABILITY_API = 'https://www.readability.com/api/rest/v1'


class ReadabilityOAuth(BaseOAuth1):
    """Readability OAuth authentication backend"""
    name = 'readability'
    ID_KEY = 'username'
    AUTHORIZATION_URL = '%s/oauth/authorize/' % READABILITY_API
    REQUEST_TOKEN_URL = '%s/oauth/request_token/' % READABILITY_API
    ACCESS_TOKEN_URL = '%s/oauth/access_token/' % READABILITY_API
    EXTRA_DATA = [('date_joined', 'date_joined'),
                  ('kindle_email_address', 'kindle_email_address'),
                  ('avatar_url', 'avatar_url'),
                  ('email_into_address', 'email_into_address')]

    def get_user_details(self, response):
        return {'username': response['username'],
                'first_name': response['first_name'],
                'last_name': response['last_name']}

    def user_data(self, access_token):
        return self.get_json(READABILITY_API + '/users/_current',
                             auth=self.oauth_auth(access_token))
