"""
Mendeley OAuth support
No extra configurations are needed to make this work.
"""
from social.backends.oauth import BaseOAuth1


class MendeleyOAuth(BaseOAuth1):
    name = 'mendeley'
    AUTHORIZATION_URL = 'http://api.mendeley.com/oauth/authorize/'
    REQUEST_TOKEN_URL = 'http://api.mendeley.com/oauth/request_token/'
    ACCESS_TOKEN_URL = 'http://api.mendeley.com/oauth/access_token/'
    SCOPE_SEPARATOR = '+'
    EXTRA_DATA = [('profile_id', 'profile_id'),
                  ('name', 'name'),
                  ('bio', 'bio')]

    def get_user_id(self, details, response):
        return response['main']['profile_id']

    def get_user_details(self, response):
        """Return user details from Mendeley account"""
        profile_id = response['main']['profile_id']
        name = response['main']['name']
        bio = response['main']['bio']
        return {'profile_id': profile_id,
                'name': name,
                'bio': bio}

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        values = self.get_json(
            'http://api.mendeley.com/oapi/profiles/info/me/',
            auth=self.oauth_auth(access_token)
        )
        values.update(values['main'])
        return values
