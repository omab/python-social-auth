"""
Twitter OAuth1 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/twitter.html
"""
from social.backends.oauth import BaseOAuth1
from social.exceptions import AuthCanceled


class TwitterOAuth(BaseOAuth1):
    """Twitter OAuth authentication backend"""
    name = 'twitter'
    EXTRA_DATA = [('id', 'id')]
    REQUEST_TOKEN_METHOD = 'POST'
    ACCESS_TOKEN_METHOD = 'POST'
    AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authenticate'
    REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
    ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
    REDIRECT_STATE = True

    def process_error(self, data):
        if 'denied' in data:
            raise AuthCanceled(self)
        else:
            super(TwitterOAuth, self).process_error(data)

    def get_user_details(self, response):
        """Return user details from Twitter account"""
        fullname, first_name, last_name = self.get_user_names(response['name'])
        return {'username': response['screen_name'],
                'email': '',  # not supplied
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        return self.get_json(
            'https://api.twitter.com/1.1/account/verify_credentials.json',
            auth=self.oauth_auth(access_token)
        )
