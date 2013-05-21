"""
Trello OAuth support.

This contribution adds support for Trello OAuth service. The settings
SOCIAL_AUTH_TRELLO_KEY and SOCIAL_AUTH_TRELLO_SECRET must be defined with
the values given by `https://trello.com/1/appKey/generate`.

Extended permissions are supported by defining TRELLO_EXTENDED_PERMISSIONS
setting, it must be a list of values to request.

By default account id and token expiration time are stored in extra_data
field, check OAuthBackend class for details on how to extend it.

"""

from social.backends.oauth import BaseOAuth1


class TrelloOAuth(BaseOAuth1):

    """Trello OAuth authentication backend"""
    name = 'trello'
    ID_KEY = 'username'
    AUTHORIZATION_URL = 'https://trello.com/1/OAuthAuthorizeToken'
    REQUEST_TOKEN_URL = 'https://trello.com/1/OAuthGetRequestToken'
    ACCESS_TOKEN_URL = 'https://trello.com/1/OAuthGetAccessToken'

    EXTRA_DATA = [
        ('username', 'username'),
        ('email', 'email'),
        ('fullName', 'fullName')
    ]

    def get_user_details(self, response):
        """Return user details from Trello account"""
        return {'username': response.get('username'),
                'email': response.get('email'),
                'fullName': response.get('fullName')}

    def user_data(self, access_token):
        """Return user data provided"""
        url = 'https://trello.com/1/members/me'
        try:
            return self.get_json(url, auth=self.oauth_auth(access_token))
        except ValueError:
            return None
