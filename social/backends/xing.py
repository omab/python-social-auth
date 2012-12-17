"""
XING OAuth support

No extra configurations are needed to make this work.
"""
import json
from urllib import urlencode

import oauth2 as oauth
from oauth2 import Token

from social.backends.oauth import ConsumerBasedOAuth
from social.exceptions import AuthCanceled, AuthUnknownError


class XingOAuth(ConsumerBasedOAuth):
    """Xing OAuth authentication backend"""
    name = 'xing'
    AUTHORIZATION_URL = 'https://www.xing.com/v1/authorize'
    REQUEST_TOKEN_URL = 'https://api.xing.com/v1/request_token'
    ACCESS_TOKEN_URL = 'https://api.xing.com/v1/access_token'
    SCOPE_SEPARATOR = '+'
    EXTRA_DATA = [
        ('id', 'id'),
        ('user_id', 'user_id')
    ]

    def get_user_details(self, response):
        """Return user details from Xing account"""
        first_name, last_name = response['first_name'], response['last_name']
        email = response.get('email', '')
        return {'username': first_name + last_name,
                'fullname': first_name + ' ' + last_name,
                'first_name': first_name,
                'last_name': last_name,
                'email': email}

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        key, secret = self.get_key_and_secret()
        consumer = oauth.Consumer(key=key, secret=secret)
        client = oauth.Client(consumer, access_token)
        url = 'https://api.xing.com/v1/users/me.json'
        resp, content = client.request(url, 'GET')

        try:
            profile = json.loads(content)['users'][0]
            return {
                'user_id': profile['id'],
                'id': profile['id'],
                'first_name': profile['first_name'],
                'last_name': profile['last_name'],
                'email': profile['active_email']
            }
        except (ValueError, KeyError, IndexError):
            pass

    def auth_complete(self, *args, **kwargs):
        """Complete auth process. Check Xing error response."""
        oauth_problem = self.data.get('oauth_problem')
        if oauth_problem:
            if oauth_problem == 'user_refused':
                raise AuthCanceled(self, '')
            else:
                raise AuthUnknownError(self, 'Xing error was %s' %
                                                    oauth_problem)
        return super(XingOAuth, self).auth_complete(*args, **kwargs)

    def unauthorized_token(self):
        """Makes first request to oauth. Returns an unauthorized Token."""
        request_token_url = self.REQUEST_TOKEN_URL
        scope = self.get_scope_argument()
        if scope:
            request_token_url = request_token_url + '?' + urlencode(scope)

        request = self.oauth_request(
            token=None,
            url=request_token_url,
            extra_params=self.request_token_extra_arguments()
        )
        response = self.fetch_response(request)
        return Token.from_string(response)


BACKENDS = {
    'xing': XingOAuth
}
