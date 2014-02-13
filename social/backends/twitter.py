"""
Twitter OAuth1 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/twitter.html
"""
from social.backends.oauth import BaseOAuth1


class TwitterOAuth(BaseOAuth1):
    """Twitter OAuth authentication backend"""
    name = 'twitter'
    EXTRA_DATA = [('id', 'id')]
    AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authenticate'
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
