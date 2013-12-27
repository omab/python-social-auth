"""
OpenStreetMap OAuth support.

This adds support for OpenStreetMap OAuth service. An application must be
registered first on OpenStreetMap and the settings
SOCIAL_AUTH_OPENSTREETMAP_KEY and SOCIAL_AUTH_OPENSTREETMAP_SECRET
must be defined with the corresponding values.

More info: http://wiki.openstreetmap.org/wiki/OAuth
"""

from xml.dom import minidom
from social.backends.oauth import BaseOAuth1

class OpenStreetMapOAuth(BaseOAuth1):
    """OpenStreetMap OAuth authentication backend"""
    name = 'openstreetmap'
    AUTHORIZATION_URL = 'http://www.openstreetmap.org/oauth/authorize'
    REQUEST_TOKEN_URL = 'http://www.openstreetmap.org/oauth/request_token'
    ACCESS_TOKEN_URL = 'http://www.openstreetmap.org/oauth/access_token'

    EXTRA_DATA = [
                  ('id','id'),
                  ('avatar','avatar'),
                  ('account_created','account_created')
                ]

    def get_user_details(self, response):
        """Return user details from OpenStreetMap account"""
        return {
            'username': response['username'],
            'email': '',
            'fullname': '',
            'first_name': '',
            'last_name': ''
            }

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        url = 'http://api.openstreetmap.org/api/0.6/user/details'
        try:
            dom = minidom.parseString(self.oauth_request(access_token,url).content)
        except ValueError:
            return None

        return {
            'id':                dom.getElementsByTagName('user')[0].getAttribute('id'),
            'username':          dom.getElementsByTagName('user')[0].getAttribute('display_name'),
            'avatar':            dom.getElementsByTagName('img')[0].getAttribute('href'),
            'account_created':   dom.getElementsByTagName('user')[0].getAttribute('account_created')
            }
