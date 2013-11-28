"""
ThisIsMyJam OAuth1 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/thisismyjam.html
"""
from social.backends.oauth import BaseOAuth1


class ThisIsMyJamOAuth1(BaseOAuth1):
    """ThisIsMyJam OAuth1 authentication backend"""
    name = 'thisismyjam'
    REQUEST_TOKEN_URL = 'http://www.thisismyjam.com/oauth/request_token'
    AUTHORIZATION_URL = 'http://www.thisismyjam.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'http://www.thisismyjam.com/oauth/access_token'
    REDIRECT_URI_PARAMETER_NAME = 'oauth_callback'

    def get_user_details(self, response):
        """Return user details from ThisIsMyJam account"""
        return {
            'username': response.get('person').get('name'),
            'fullname': response.get('person').get('fullname'),
            'email': '',
            'first_name': '',
            'last_name': ''
        }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json('http://api.thisismyjam.com/1/verify.json',
                             auth=self.oauth_auth(access_token))
