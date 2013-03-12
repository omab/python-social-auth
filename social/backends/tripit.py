"""
TripIt OAuth support.

This adds support for TripIt OAuth service. An application must
be registered first on TripIt and the settings TRIPIT_API_KEY
and TRIPIT_API_SECRET must be defined with the corresponding
values.

User screen name is used to generate username.
"""
from xml.dom import minidom

from social.backends.oauth import BaseOAuth1


class TripItOAuth(BaseOAuth1):
    """TripIt OAuth authentication backend"""
    name = 'tripit'
    AUTHORIZATION_URL = 'https://www.tripit.com/oauth/authorize'
    REQUEST_TOKEN_URL = 'https://api.tripit.com/oauth/request_token'
    ACCESS_TOKEN_URL = 'https://api.tripit.com/oauth/access_token'
    EXTRA_DATA = [('screen_name', 'screen_name')]

    def get_user_details(self, response):
        """Return user details from TripIt account"""
        try:
            first_name, last_name = response['name'].split(' ', 1)
        except ValueError:
            first_name = response['name']
            last_name = ''
        return {'username': response['screen_name'],
                'email': response['email'],
                'fullname': response['name'],
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        url = 'https://api.tripit.com/v1/get/profile'
        content = self.oauth_request(access_token, url).content
        try:
            dom = minidom.parseString(content)
        except ValueError:
            return None

        return {
            'id': dom.getElementsByTagName('Profile')[0].getAttribute('ref'),
            'name': dom.getElementsByTagName('public_display_name')[0]
                                    .childNodes[0].data,
            'screen_name': dom.getElementsByTagName('screen_name')[0]
                                    .childNodes[0].data,
            'email': dom.getElementsByTagName('is_primary')[0]
                                    .parentNode
                                        .getElementsByTagName('address')[0]
                                            .childNodes[0].data
        }
