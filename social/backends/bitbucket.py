"""
Bitbucket OAuth1 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/bitbucket.html
"""
from social.exceptions import AuthForbidden
from social.backends.oauth import BaseOAuth1


class BitbucketOAuth(BaseOAuth1):
    """Bitbucket OAuth authentication backend"""
    name = 'bitbucket'
    ID_KEY = 'uuid'
    AUTHORIZATION_URL = 'https://bitbucket.org/api/1.0/oauth/authenticate'
    REQUEST_TOKEN_URL = 'https://bitbucket.org/api/1.0/oauth/request_token'
    ACCESS_TOKEN_URL = 'https://bitbucket.org/api/1.0/oauth/access_token'

    def get_user_id(self, details, response):
        id_key = self.ID_KEY
        if self.setting('USERNAME_AS_ID', False):
            id_key = 'username'
        return response.get(id_key)

    def get_user_details(self, response):
        """Return user details from Bitbucket account"""
        fullname, first_name, last_name = self.get_user_names(
            response['display_name']
        )

        return {'username': response.get('username', ''),
                'email': response.get('email', ''),
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token):
        """Return user data provided"""
        emails = self.get_json('https://api.bitbucket.org/2.0/user/emails',
                               auth=self.oauth_auth(access_token))

        email = None

        for address in reversed(emails['values']):
            email = address['email']
            if address['is_primary']:
                break

        if self.setting('VERIFIED_EMAILS_ONLY', False) and not address['is_confirmed']:
            raise AuthForbidden(
                self, 'Bitbucket account has no verified email'
            )

        user = self.get_json('https://api.bitbucket.org/2.0/user',
                             auth=self.oauth_auth(access_token))

        if email:
            user['email'] = email

        return user
