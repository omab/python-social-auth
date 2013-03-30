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
from social.exceptions import AuthCanceled
from social.backends.oauth import BaseOAuth1


class TwitterOAuth(BaseOAuth1):
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
        return self.get_json(
            'https://api.twitter.com/1.1/account/verify_credentials.json',
            auth=self.oauth_auth(access_token)
        )

    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""
        if 'denied' in self.data:
            raise AuthCanceled(self)
        return super(TwitterOAuth, self).auth_complete(*args, **kwargs)
