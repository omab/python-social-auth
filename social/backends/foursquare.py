import json
from urllib import urlencode

from social.backends.oauth import BaseOAuth2


class FoursquareOAuth2(BaseOAuth2):
    name = 'foursquare'
    AUTHORIZATION_URL = 'https://foursquare.com/oauth2/authenticate'
    ACCESS_TOKEN_URL = 'https://foursquare.com/oauth2/access_token'

    def get_user_id(self, details, response):
        return response['response']['user']['id']

    def get_user_details(self, response):
        """Return user details from Foursquare account"""
        firstName = response['response']['user']['firstName']
        lastName = response['response']['user'].get('lastName', '')
        email = response['response']['user']['contact']['email']
        return {'username': firstName + ' ' + lastName,
                'first_name': firstName,
                'last_name': lastName,
                'email': email}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://api.foursquare.com/v2/users/self?' + urlencode({
            'oauth_token': access_token
        })
        try:
            return json.load(self.urlopen(url))
        except ValueError:
            return None
