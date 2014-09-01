"""
Spotify backend, docs at:
    https://developer.spotify.com/spotify-web-api/
    https://developer.spotify.com/spotify-web-api/authorization-guide/
"""
import base64

from social.backends.oauth import BaseOAuth2


class SpotifyOAuth2(BaseOAuth2):
    name = 'spotify'
    SCOPE_SEPARATOR = ' '
    ID_KEY = 'id'
    AUTHORIZATION_URL = 'https://accounts.spotify.com/authorize'
    ACCESS_TOKEN_URL = 'https://accounts.spotify.com/api/token'
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False

    def auth_headers(self):
        return {
            'Authorization': 'Basic {0}'.format(base64.urlsafe_b64encode(
                ('{0}:{1}'.format(*self.get_key_and_secret()).encode())
            ))
        }

    def get_user_details(self, response):
        """Return user details from Spotify account"""
        fullname, first_name, last_name = self.get_user_names(
            response.get('display_name')
        )
        return {'username': response.get('id'),
                'email': response.get('email'),
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json(
            'https://api.spotify.com/v1/me',
            headers={'Authorization': 'Bearer {0}'.format(access_token)}
        )
