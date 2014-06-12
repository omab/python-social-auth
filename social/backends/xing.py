"""
XING OAuth1 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/xing.html
"""
from social.backends.oauth import BaseOAuth1


class XingOAuth(BaseOAuth1):
    """Xing OAuth authentication backend"""
    name = 'xing'
    AUTHORIZATION_URL = 'https://api.xing.com/v1/authorize'
    REQUEST_TOKEN_URL = 'https://api.xing.com/v1/request_token'
    ACCESS_TOKEN_URL = 'https://api.xing.com/v1/access_token'
    SCOPE_SEPARATOR = '+'
    EXTRA_DATA = [
        ('id', 'id'),
        ('user_id', 'user_id')
    ]

    def get_user_details(self, response):
        """Return user details from Xing account"""
        email = response.get('email', '')
        fullname, first_name, last_name = self.get_user_names(
            first_name=response['first_name'],
            last_name=response['last_name']
        )
        return {'username': first_name + last_name,
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name,
                'email': email}

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        profile = self.get_json(
            'https://api.xing.com/v1/users/me.json',
            auth=self.oauth_auth(access_token)
        )['users'][0]
        return {
            'user_id': profile['id'],
            'id': profile['id'],
            'first_name': profile['first_name'],
            'last_name': profile['last_name'],
            'email': profile['active_email']
        }
