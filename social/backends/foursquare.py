"""
Foursquare OAuth2 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/foursquare.html
"""
from social.backends.oauth import BaseOAuth2


class FoursquareOAuth2(BaseOAuth2):
    name = 'foursquare'
    AUTHORIZATION_URL = 'https://foursquare.com/oauth2/authenticate'
    ACCESS_TOKEN_URL = 'https://foursquare.com/oauth2/access_token'
    ACCESS_TOKEN_METHOD = 'POST'
    API_VERSION = '20140128'

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
        return self.get_json('https://api.foursquare.com/v2/users/self',
                             params={'oauth_token': access_token,
                                     'v': self.API_VERSION})
