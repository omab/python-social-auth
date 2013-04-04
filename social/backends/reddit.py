"""
Reddit OAuth2 support as detailed at:
    https://github.com/reddit/reddit/wiki/OAuth2
"""
import base64

from social.backends.oauth import BaseOAuth2


class RedditOAuth2(BaseOAuth2):
    """Reddit OAuth2 authentication backend"""
    name = 'reddit'
    AUTHORIZATION_URL = 'https://ssl.reddit.com/api/v1/authorize'
    ACCESS_TOKEN_URL = 'https://ssl.reddit.com/api/v1/access_token'
    ACCESS_TOKEN_METHOD = 'POST'
    REFRESH_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False
    SCOPE_SEPARATOR = ','
    DEFAULT_SCOPE = ['identity']
    EXTRA_DATA = [
        ('id', 'id'),
        ('link_karma', 'link_karma'),
        ('comment_karma', 'comment_karma'),
        ('refresh_token', 'refresh_token'),
        ('expires_in', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from Github account"""
        return {'username': response.get('name'),
                'email': '', 'fullname': '',
                'first_name': '', 'last_name': ''}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json(
            'https://oauth.reddit.com/api/v1/me.json',
            headers={'Authorization': 'bearer ' + access_token}
        )

    def auth_headers(self):
        return {
            'Authorization': 'Basic %s' % base64.urlsafe_b64encode(
                ('%s:%s' % self.get_key_and_secret()).encode()
            )
        }

    def refresh_token_params(self, token, redirect_uri=None, *args, **kwargs):
        params = super(RedditOAuth2, self).refresh_token_params(token)
        params['redirect_uri'] = self.redirect_uri or redirect_uri
        return params
