"""
Live OAuth2 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/live.html
"""
from social.backends.oauth import BaseOAuth2


class LiveOAuth2(BaseOAuth2):
    name = 'live'
    AUTHORIZATION_URL = 'https://login.live.com/oauth20_authorize.srf'
    ACCESS_TOKEN_URL = 'https://login.live.com/oauth20_token.srf'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','
    DEFAULT_SCOPE = ['wl.basic', 'wl.emails']
    EXTRA_DATA = [
        ('id', 'id'),
        ('access_token', 'access_token'),
        ('authentication_token', 'authentication_token'),
        ('refresh_token', 'refresh_token'),
        ('expires_in', 'expires'),
        ('email', 'email'),
        ('first_name', 'first_name'),
        ('last_name', 'last_name'),
        ('token_type', 'token_type'),
    ]

    def get_user_details(self, response):
        """Return user details from Live Connect account"""
        return {'username': response.get('name'),
                'email': response.get('emails', {}).get('account', ''),
                'first_name': response.get('first_name'),
                'last_name': response.get('last_name')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json('https://apis.live.net/v5.0/me', params={
            'access_token': access_token
        })
