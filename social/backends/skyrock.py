"""
Skyrock OAuth1 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/skyrock.html
"""
from social.backends.oauth import BaseOAuth1


class SkyrockOAuth(BaseOAuth1):
    """Skyrock OAuth authentication backend"""
    name = 'skyrock'
    ID_KEY = 'id_user'
    AUTHORIZATION_URL = 'https://api.skyrock.com/v2/oauth/authenticate'
    REQUEST_TOKEN_URL = 'https://api.skyrock.com/v2/oauth/initiate'
    ACCESS_TOKEN_URL = 'https://api.skyrock.com/v2/oauth/token'
    EXTRA_DATA = [('id', 'id')]

    def get_user_details(self, response):
        """Return user details from Skyrock account"""
        return {'username': response['username'],
                'email': response['email'],
                'fullname': response['firstname'] + ' ' + response['name'],
                'first_name': response['firstname'],
                'last_name': response['name']}

    def user_data(self, access_token):
        """Return user data provided"""
        return self.get_json('https://api.skyrock.com/v2/user/get.json',
                             auth=self.oauth_auth(access_token))
