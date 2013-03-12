"""
Bitbucket OAuth support.

This adds support for Bitbucket OAuth service. An application must
be registered first on Bitbucket and the settings BITBUCKET_CONSUMER_KEY
and BITBUCKET_CONSUMER_SECRET must be defined with the corresponding
values.

By default username, email, token expiration time, first name and last name are
stored in extra_data field, check OAuthBackend class for details on how to
extend it.
"""
from social.backends.oauth import BaseOAuth1


class BitbucketOAuth(BaseOAuth1):
    """Bitbucket OAuth authentication backend"""
    name = 'bitbucket'
    ID_KEY = 'username'
    AUTHORIZATION_URL = 'https://bitbucket.org/api/1.0/oauth/authenticate'
    REQUEST_TOKEN_URL = 'https://bitbucket.org/api/1.0/oauth/request_token'
    ACCESS_TOKEN_URL = 'https://bitbucket.org/api/1.0/oauth/access_token'
    EXTRA_DATA = [
        ('username', 'username'),
        ('expires', 'expires'),
        ('email', 'email'),
        ('first_name', 'first_name'),
        ('last_name', 'last_name')
    ]

    def get_user_details(self, response):
        """Return user details from Bitbucket account"""
        return {'username': response.get('username'),
                'email': response.get('email'),
                'fullname': ' '.join((response.get('first_name'),
                                      response.get('last_name'))),
                'first_name': response.get('first_name'),
                'last_name': response.get('last_name')}

    @classmethod
    def tokens(cls, instance):
        """Return the tokens needed to authenticate the access to any API the
        service might provide. Bitbucket uses a pair of OAuthToken consisting
        on a oauth_token and oauth_token_secret.

        instance must be a UserSocialAuth instance.
        """
        token = super(BitbucketOAuth, cls).tokens(instance)
        if token and 'access_token' in token:
            token = dict(tok.split('=')
                            for tok in token['access_token'].split('&'))
        return token

    def user_data(self, access_token):
        """Return user data provided"""
        # Bitbucket has a bit of an indirect route to obtain user data from an
        # authenticated query: First obtain the user's email via an
        # authenticated GET
        try:
            # Then retrieve the user's primary email address or the top email
            email_addresses = self.get_json(
                'https://bitbucket.org/api/1.0/emails/',
                auth=self.oauth_auth(access_token)
            )
            for email_address in reversed(email_addresses):
                if email_address['active']:
                    email = email_address['email']
                    if email_address['primary']:
                        break
            url = 'https://bitbucket.org/api/1.0/users/'
            return dict(self.get_json(url + email)['user'], email=email)
        except ValueError:
            return None
        return None
