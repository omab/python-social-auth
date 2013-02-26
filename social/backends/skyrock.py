"""
Skyrock OAuth support.

This adds support for Skyrock OAuth service. An application must
be registered first on skyrock and the settings SKYROCK_CONSUMER_KEY
and SKYROCK_CONSUMER_SECRET must be defined with they corresponding
values.

By default account id is stored in extra_data field, check OAuthBackend
class for details on how to extend it.
"""
import json

from social.backends import ConsumerBasedOAuth


class SkyrockOAuth(ConsumerBasedOAuth):
    """Skyrock OAuth authentication backend"""
    name = 'skyrock'
    ID_KEY = 'id_user'
    AUTHORIZATION_URL = 'https://api.skyrock.com/v2/oauth/authenticate'
    REQUEST_TOKEN_URL = 'https://api.skyrock.com/v2/oauth/initiate'
    ACCESS_TOKEN_URL = 'https://api.skyrock.com/v2/oauth/token'
    EXTRA_DATA = [('id', 'id')]

    def get_user_details(self, response):
        """Return user details from Skyrock account"""
        return {'username': response['username'],
                'email': response['email'],
                'fullname': response['firstname'] + ' ' + response['name'],
                'first_name': response['firstname'],
                'last_name': response['name']}

    def user_data(self, access_token):
        """Return user data provided"""
        url = 'https://https://api.skyrock.com/v2/user/get.json'
        request = self.oauth_request(access_token, url)
        try:
            return json.loads(self.fetch_response(request))
        except ValueError:
            return None

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        if 'denied' in self.data:
            raise ValueError('Authentication denied')
        else:
            return super(SkyrockOAuth, self).auth_complete(*args, **kwargs)
