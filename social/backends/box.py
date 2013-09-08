"""
Box.net OAuth support.

This contribution adds support for GitHub OAuth service. The settings
SOCIAL_AUTH_BOX_KEY and SOCIAL_AUTH_BOX_SECRET must be defined with the values
given by Box.net application registration process.

Extended permissions are supported by defining BOX_EXTENDED_PERMISSIONS
setting, it must be a list of values to request.

By default account id and token expiration time are stored in extra_data
field, check OAuthBackend class for details on how to extend it.
"""
from social.backends.oauth import BaseOAuth2


class BoxOAuth2(BaseOAuth2):
    """Box.net OAuth authentication backend"""
    name = 'box'
    AUTHORIZATION_URL = 'https://www.box.com/api/oauth2/authorize'
    ACCESS_TOKEN_METHOD = 'POST'
    ACCESS_TOKEN_URL = 'https://www.box.com/api/oauth2/token'
    REVOKE_TOKEN_URL = 'https://www.box.com/api/oauth2/revoke'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token', True),
        ('id', 'id'),
        ('expires', 'expires'),
        ('created_at', 'created_at'),
        ('modified_at', 'modified_at'),
        ('status', 'status'),
        ('type', 'type'),
        ('language', 'language'),
        ('avatar_url', 'avatar_url'),
        ('max_upload_size', 'max_upload_size'),
        ('space_amount', 'space_amount'),
        ('space_used', 'space_used'),
    ]

    def do_auth(self, access_token, response=None, *args, **kwargs):
        response = response or {}
        data = self.user_data(access_token)

        data['access_token'] = response.get('access_token')
        data['refresh_token'] = response.get('refresh_token')
        data['expires'] = response.get('expires_in')
        kwargs.update({'backend': self, 'response': data})
        return self.strategy.authenticate(*args, **kwargs)

    def get_user_details(self, response):
        """Return user details Box.net account"""
        return {'username': response.get('login'),
                'email': response.get('login') or '',
                'first_name': response.get('name')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        params = self.setting('PROFILE_EXTRA_PARAMS', {})
        params['access_token'] = access_token
        return self.get_json('https://api.box.com/2.0/users/me',
                             params=params)

    def refresh_token(self, token, *args, **kwargs):
        params = self.refresh_token_params(token, *args, **kwargs)
        request = self.request(self.REFRESH_TOKEN_URL or self.ACCESS_TOKEN_URL,
                               data=params, headers=self.auth_headers(),
                               method='POST')
        return self.process_refresh_token_response(request, *args, **kwargs)
