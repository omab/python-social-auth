"""
Khan Academy OAuth backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/facebook.html
"""

from social.backends.oauth import BaseOAuth1


class KhanAcademyOAuth1(BaseOAuth1):
    name = 'khanacademy-oauth'
    ID_KEY = 'user_id'
    AUTHORIZATION_URL = 'https://www.khanacademy.org/api/auth'
    REQUEST_TOKEN_URL = 'https://www.khanacademy.org/api/auth/request_token'
    ACCESS_TOKEN_URL = 'https://www.khanacademy.org/api/auth/access_token'
    REDIRECT_URI_PARAMETER_NAME = 'oauth_callback'

    def get_user_details(self, response):
        """Return user details from Facebook account"""
        return {
            'username': response.get('key_email'),
            'email': response.get('key_email'),
            'fullname': '',
            'first_name': '',
            'last_name': '',
            'user_id': response.get('user_id')
        }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json('https://www.khanacademy.org/api/v1/user',
                             auth=self.oauth_auth(access_token))
