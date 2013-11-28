"""
Bitbucket OAuth1 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/bitbucket.html
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

    def user_data(self, access_token):
        """Return user data provided"""
        # Bitbucket has a bit of an indirect route to obtain user data from an
        # authenticated query: First obtain the user's email via an
        # authenticated GET, then retrieve the user's primary email address or
        # the top email
        emails = self.get_json('https://bitbucket.org/api/1.0/emails/',
                               auth=self.oauth_auth(access_token))
        for address in reversed(emails):
            if address['active']:
                email = address['email']
                if address['primary']:
                    break
        return dict(self.get_json('https://bitbucket.org/api/1.0/users/' +
                                  email)['user'],
                    email=email)
