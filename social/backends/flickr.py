"""
Flickr OAuth support.

This contribution adds support for Flickr OAuth service. The settings
FLICKR_APP_ID and FLICKR_API_SECRET must be defined with the values
given by Flickr application registration process.

By default account id, username and token expiration time are stored in
extra_data field, check OAuthBackend class for details on how to extend it.
"""
from social.backends.oauth import BaseOAuth1


class FlickrOAuth(BaseOAuth1):
    """Flickr OAuth authentication backend"""
    name = 'flickr'
    AUTHORIZATION_URL = 'http://www.flickr.com/services/oauth/authorize'
    REQUEST_TOKEN_URL = 'http://www.flickr.com/services/oauth/request_token'
    ACCESS_TOKEN_URL = 'http://www.flickr.com/services/oauth/access_token'
    EXTRA_DATA = [
        ('id', 'id'),
        ('username', 'username'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from Flickr account"""
        return {'username': response.get('id'),
                'email': '',
                'first_name': response.get('fullname')}

    def access_token(self, token):
        """Return request for access token value"""
        # Flickr is a bit different - it passes user information along with
        # the access token, so temporarily store it to view the user_data
        # method easy access later in the flow!
        return self.get_querystring(self.ACCESS_TOKEN_URL,
                                    auth=self.oauth_auth(token))

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return {
            'id': access_token['user_nsid'],
            'username': access_token['username'],
            'fullname': access_token.get('fullname', ''),
        }

    def auth_extra_arguments(self):
        params = super(FlickrOAuth, self).auth_extra_arguments() or {}
        if not 'perms' in params:
            params['perms'] = 'read'
        return params
