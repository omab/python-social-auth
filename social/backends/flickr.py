"""
Flickr OAuth1 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/flickr.html
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
        return {'username': response.get('username') or response.get('id'),
                'email': '',
                'first_name': response.get('fullname')}

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
