"""
Twitter OAuth support.

This adds support for Twitter OAuth service. An application must
be registered first on twitter and the settings TWITTER_CONSUMER_KEY
and TWITTER_CONSUMER_SECRET must be defined with the corresponding
values.

User screen name is used to generate username.

By default account id is stored in extra_data field, check OAuthBackend
class for details on how to extend it.
"""
import json

from social.exceptions import AuthCanceled
from social.backends.oauth import ConsumerBasedOAuth


class TwitterOAuth(ConsumerBasedOAuth):
    """Twitter OAuth authentication backend"""
    name = 'twitter'
    EXTRA_DATA = [('id', 'id')]
    AUTHORIZATION_URL = 'http://api.twitter.com/oauth/authenticate'
    REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
    ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'

    def get_user_details(self, response):
        """Return user details from Twitter account"""
        try:
            first_name, last_name = response['name'].split(' ', 1)
        except:
            first_name = response['name']
            last_name = ''
        return {'username': response['screen_name'],
                'email': '',  # not supplied
                'fullname': response['name'],
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
        response = self.fetch_response(self.oauth_request(access_token, url))
        try:
            return json.loads(response)
        except ValueError:
            return None

    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""
        if 'denied' in self.data:
            raise AuthCanceled(self)
        return super(TwitterOAuth, self).auth_complete(*args, **kwargs)

    @classmethod
    def tokens(cls, instance):
        """Return the tokens needed to authenticate the access to any API the
        service might provide. Twitter uses a pair of OAuthToken consisting of
        an oauth_token and oauth_token_secret.

        instance must be a UserSocialAuth instance.
        """
        token = super(TwitterOAuth, cls).tokens(instance)
        if token and 'access_token' in token:
            token = dict(tok.split('=')
                            for tok in token['access_token'].split('&'))
        return token
