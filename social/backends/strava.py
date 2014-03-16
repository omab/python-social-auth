"""
Strava OAuth2 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/strava.html
"""
from social.backends.oauth import BaseOAuth2


class StravaOAuth(BaseOAuth2):
    name = 'strava'
    AUTHORIZATION_URL = 'https://www.strava.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://www.strava.com/oauth/token'
    ACCESS_TOKEN_METHOD = 'POST'

    def get_user_id(self, details, response):
        return response['athlete']['id']

    def get_user_details(self, response):
        """Return user details from Strava account"""
        # because there is no usernames on strava
        username = response['athlete']['id']
        first_name = response['athlete'].get('first_name', '')
        email = response['athlete'].get('email', '')
        return {'username': str(username),
                'first_name': first_name,
                'email': email}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json('https://www.strava.com/api/v3/athlete',
                             params={'access_token': access_token})
