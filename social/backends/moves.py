"""
Moves OAuth2 backend, docs at:
    https://dev.moves-app.com/docs/authentication

Written by Avi Alkalay <avi at unix dot sh>
Certified to work with Django 1.6
"""
from social.backends.oauth import BaseOAuth2


class MovesOAuth2(BaseOAuth2):
    """Moves OAuth authentication backend"""
    name = 'moves'

    # From https://dev.moves-app.com/docs/authentication#authorization
    AUTHORIZATION_URL = 'https://api.moves-app.com/oauth/v1/authorize'
    ACCESS_TOKEN_URL = 'https://api.moves-app.com/oauth/v1/access_token?grant_type=authorization_code'
    REFRESH_TOKEN_URL = 'https://api.moves-app.com/oauth/v1/access_token?grant_type=refresh_token'

    ID_KEY = 'user_id'
    REDIRECT_STATE = True
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ' '
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token', True),
        ('expires_in', 'expires'),
        ('firstDate', 'firstdate')
    ]

    def get_user_details(self, response):
        """Return user details Moves account"""
        return {'username': response.get('user_id')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        params = self.setting('PROFILE_EXTRA_PARAMS', {})
        params['access_token'] = access_token
        return self.get_json('https://api.moves-app.com/api/1.1/user/profile',
            params=params)

    def refresh_token(self, token, *args, **kwargs):
        params = self.refresh_token_params(token, *args, **kwargs)
        request = self.request(self.REFRESH_TOKEN_URL or self.ACCESS_TOKEN_URL,
                               data=params, headers=self.auth_headers(),
                               method='POST')
        return self.process_refresh_token_response(request, *args, **kwargs)
