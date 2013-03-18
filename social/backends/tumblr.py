"""
Tumblr OAuth 1.0a support.

Take a look to http://www.tumblr.com/docs/en/api/v2

You need to register OAuth site here: http://www.tumblr.com/oauth/apps

Then update your settings values using registration information

ref:
    https://github.com/gkmngrgn/django-tumblr-auth
"""
from social.utils import first
from social.backends.oauth import BaseOAuth1


class TumblrOAuth(BaseOAuth1):
    name = 'tumblr'
    ID_KEY = 'username'
    AUTHORIZATION_URL = 'http://www.tumblr.com/oauth/authorize'
    REQUEST_TOKEN_URL = 'http://www.tumblr.com/oauth/request_token'
    REQUEST_TOKEN_METHOD = 'POST'
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
        try:
            return self.get_json('http://api.tumblr.com/v2/user/info',
                                 auth=self.oauth_auth(access_token))
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
