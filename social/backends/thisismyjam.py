"""
ThisIsMyJam OAuth support.

This contribution adds support for ThisIsMyJam service.

The settings SOCIAL_AUTH_THISISMYJAM_KEY & SOCIAL_AUTH_THISISMYJAM_SECRET must be defined
with the values given by SoundCloud application registration process.

http://www.thisismyjam.com/developers

By default account id and token expiration time are stored in extra_data
field, check OAuthBackend class for details on how to extend it.
"""

from social.p3 import urlencode
from social.backends.oauth import BaseOAuth1


class ThisIsMyJamOAuth1(BaseOAuth1):
    """Soundcloud OAuth authentication backend"""
    name = "thisismyjam"
    REQUEST_TOKEN_URL = "http://www.thisismyjam.com/oauth/request_token"
    AUTHORIZATION_URL = "http://www.thisismyjam.com/oauth/authorize"
    ACCESS_TOKEN_URL = "http://www.thisismyjam.com/oauth/access_token"
    REDIRECT_URI_PARAMETER_NAME="oauth_callback"

    def get_user_details(self, response):
        """Return user details from ThisIsMyJam account"""
        return {'username': response.get("person").get("name"),
                'fullname': response.get("person").get("fullname"),
                'email':'',
                'first_name':'',
                'last_name':''
            }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json('http://api.thisismyjam.com/1/verify.json',
                             auth=self.oauth_auth(access_token)
                         )
