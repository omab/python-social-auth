import json
from urllib import urlencode

from social.backends.oauth import BaseOAuth2


class StocktwitsOAuth2(BaseOAuth2):
    """Stockwiths OAuth2 backend"""
    name = 'stocktwits'
    AUTHORIZATION_URL = 'https://api.stocktwits.com/api/2/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://api.stocktwits.com/api/2/oauth/token'
    SCOPE_SEPARATOR = ','
    DEFAULT_SCOPE = ['read', 'publish_messages', 'publish_watch_lists',
                     'follow_users', 'follow_stocks']

    def get_user_id(self, details, response):
        return response['user']['id']

    def get_user_details(self, response):
        """Return user details from Stocktwits account"""
        try:
            first_name, last_name = response['user']['name'].split(' ', 1)
        except:
            first_name = response['user']['name']
            last_name = ''
        return {'username': response['user']['username'],
                'email': '',  # not supplied
                'fullname': response['user']['name'],
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://api.stocktwits.com/api/2/account/verify.json?' + \
                    urlencode({'access_token': access_token})
        try:
            return json.load(self.urlopen(url))
        except ValueError:
            return None
