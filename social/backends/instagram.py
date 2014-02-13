"""
Instagram OAuth2 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/instagram.html
"""
from social.backends.oauth import BaseOAuth2


class InstagramOAuth2(BaseOAuth2):
    name = 'instagram'
    AUTHORIZATION_URL = 'https://instagram.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://instagram.com/oauth/access_token'
    ACCESS_TOKEN_METHOD = 'POST'

    def get_user_id(self, details, response):
        return response['user']['id']

    def get_user_details(self, response):
        """Return user details from Instagram account"""
        username = response['user']['username']
        fullname = response['user'].get('full_name', '')
        email = response['user'].get('email', '')
        return {'username': username,
                'first_name': fullname,
                'email': email}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json('https://api.instagram.com/v1/users/self',
                             params={'access_token': access_token})
