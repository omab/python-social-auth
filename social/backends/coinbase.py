"""
Coinbase OAuth2 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/coinbase.html
"""
from social.backends.oauth import BaseOAuth2


class CoinbaseOAuth2(BaseOAuth2):
    name = 'coinbase'
    SCOPE_SEPARATOR = '+'
    DEFAULT_SCOPE = ['user', 'balance']
    AUTHORIZATION_URL = 'https://coinbase.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://coinbase.com/oauth/token'
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False

    def get_user_id(self, details, response):
        return response['users'][0]['user']['id']

    def get_user_details(self, response):
        """Return user details from Coinbase account"""
        user_data = response['users'][0]['user']
        name = user_data['name']
        name_split = name.split()
        first_name = name_split[0]
        last_name = name_split[1]
        email = user_data.get('email', '')
        return {'username': name,
                'first_name': first_name,
                'last_name': last_name,
                'email': email}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json('https://coinbase.com/api/v1/users',
                             params={'access_token': access_token})
