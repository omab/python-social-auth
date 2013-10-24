"""
RunKeeper OAuth support.

This contribution adds support for RunKeeper Oauth service. The settings
SOCIAL_AUTH_RUNKEEPER_KEY and SOCIAL_AUTH_RUNKEEPER_SECRET must be defined with the values
given by RunKeeper application registration process.

"""
from social.backends.oauth import BaseOAuth2


class RunKeeperOAuth2(BaseOAuth2):
    """RunKeeper OAuth authentication backend"""
    name = 'runkeeper'
    AUTHORIZATION_URL = 'https://runkeeper.com/apps/authorize'
    ACCESS_TOKEN_URL = 'https://runkeeper.com/apps/token'
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('userID', 'id'),
    ]

    def get_user_id(self, details, response):
        return response['userID']

    def get_user_details(self, response):
        """
        parse username from profile link
        """
        username = None
        profile_url = response.get('profile')
        if len(profile_url):
            profile_url_parts = profile_url.split('http://runkeeper.com/user/')
            if len(profile_url_parts) > 1 and len(profile_url_parts[1]):
                username = profile_url_parts[1]

        return {'username': username,
                'email': response.get('email') or '',
                'first_name': response.get('name')}

    def user_data(self, access_token, *args, **kwargs):
        """
        We need to use the /user endpoint to get the user id
        """
        user_data = self._user_data(access_token, '/user')
        
        """
        The /profile endpoint contains name, user name, location, gender
        """
        profile_data = self._user_data(access_token, '/profile')

        data = dict(user_data.items() + profile_data.items())
        return data

    def _user_data(self, access_token, path):
        url = 'https://api.runkeeper.com{0}'.format(path)
        return self.get_json(url, params={'access_token': access_token})
