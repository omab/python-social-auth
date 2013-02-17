"""
Readability OAuth support.

This contribution adds support for Readability OAuth service. The settings
SOCIAL_AUTH_READABILITY_CONSUMER_KEY and
SOCIAL_AUTH_READABILITY_CONSUMER_SECRET must be defined with the values given
by Readability in the Connections page of your account settings."""

import json

from social.backends import ConsumerBasedOAuth
from social.exceptions import AuthCanceled


READABILITY_API = 'https://www.readability.com/api/rest/v1/'
READABILITY_USER_DATA_URL = '%s/users/_current' % READABILITY_API


class ReadabilityOAuth(ConsumerBasedOAuth):
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
        username = response['username']
        first_name, last_name = response['first_name'], response['last_name']
        return {'username': username,
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token):
        request = self.oauth_request(
            access_token, '%s/users/_current' % READABILITY_API
        )
        try:
            return json.loads(self.fetch_response(request))
        except ValueError:
            return None

    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""
        if 'error' in self.data:
            raise AuthCanceled(self)
        else:
            return super(ReadabilityOAuth, self).auth_complete(*args, **kwargs)

    @classmethod
    def tokens(cls, instance):
        """Return the tokens needed to authenticate the access to any API the
        service might provide. Readability uses a pair of OAuthToken consisting
        of an oauth_token and oauth_token_secret.

        instance must be a UserSocialAuth instance.
        """
        token = super(ReadabilityOAuth, cls).tokens(instance)
        if token and 'access_token' in token:
            # Split the OAuth query string and only return the values needed
            token = dict(filter(lambda x: x[0] in ['oauth_token',
                                                   'oauth_token_secret'],
                         map(lambda x: x.split('='),
                             token['access_token'].split('&'))))
        return token


BACKENDS = {
    'readability': ReadabilityOAuth
}
