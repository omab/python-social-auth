"""
Tumblr OAuth 1.0a support.

Take a look to http://www.tumblr.com/docs/en/api/v2

You need to register OAuth site here: http://www.tumblr.com/oauth/apps

Then update your settings values using registration information

ref:
    https://github.com/gkmngrgn/django-tumblr-auth
"""
import json

from social.utils import first
from social.backends.oauth import ConsumerBasedOAuth


class TumblrOAuth(ConsumerBasedOAuth):
    name = 'tumblr'
    ID_KEY = 'username'
    AUTHORIZATION_URL = 'http://www.tumblr.com/oauth/authorize'
    REQUEST_TOKEN_URL = 'http://www.tumblr.com/oauth/request_token'
    ACCESS_TOKEN_URL = 'http://www.tumblr.com/oauth/access_token'

    def get_user_details(self, response):
        # http://www.tumblr.com/docs/en/api/v2#user-methods
        user_info = response['response']['user']
        data = {'username': user_info['name']}
        blog = first(lambda blog: blog['primary'], user_info['blogs'])
        if blog:
            data['fullname'] = blog['title']
        return data

    def user_data(self, access_token):
        request = self.oauth_request(access_token,
                                     'http://api.tumblr.com/v2/user/info')
        try:
            return json.loads(self.fetch_response(request))
        except ValueError:
            return None

    @classmethod
    def tokens(cls, instance):
        """
        Return the tokens needed to authenticate the access to any API the
        service might provide. Tumblr uses a pair of OAuthToken consisting
        on a oauth_token and oauth_token_secret.

        instance must be a UserSocialAuth instance.
        """
        token = super(TumblrOAuth, cls).tokens(instance)
        if token and 'access_token' in token:
            token = dict(tok.split('=')
                            for tok in token['access_token'].split('&'))
        return token


BACKENDS = {
    'tumblr': TumblrOAuth
}
