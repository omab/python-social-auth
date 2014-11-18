"""
Khan Academy OAuth backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/facebook.html
"""

from oauthlib.oauth1 import Client, SIGNATURE_HMAC, SIGNATURE_TYPE_QUERY
from social.backends.oauth import BaseOAuth1


class KhanAcademyOAuth1(BaseOAuth1):
    """
    Class used for autorising with Khan Academy.

    Flow of Khan Academy is a bit different than most OAuth 1.0 and consinsts
    of the following steps:
    1. Create signed params to attach to the REQUEST_TOKEN_URL
    2. Redirect user to the REQUEST_TOKEN_URL that will respond with
       oauth_secret, oauth_token, oauth_verifier that should be used with
       ACCESS_TOKEN_URL
    3. Go to ACCESS_TOKEN_URL and grab oauth_token_secret.

    Note that we don't use the AUTHORIZATION_URL.

    AUTHORIZATION_URL requires the following arguments:
    oauth_consumer_key - Your app's consumer key
    oauth_nonce - Random 64-bit, unsigned number encoded as an ASCII string
        in decimal format. The nonce/timestamp pair should always be unique.
    oauth_version - OAuth version used by your app. Must be "1.0" for now.
    oauth_signature - String generated using the referenced signature method.
    oauth_signature_method - Signature algorithm (currently only support
        "HMAC-SHA1")
    oauth_timestamp - Integer representing the time the request is sent.
        The timestamp should be expressed in number of seconds
        after January 1, 1970 00:00:00 GMT.
    oauth_callback (optional) - URL to redirect to after request token is
        received and authorized by the user's chosen identity provider.
    """
    name = 'khanacademy-oauth1'
    ID_KEY = 'user_id'
    REQUEST_TOKEN_URL = 'http://www.khanacademy.org/api/auth/request_token'
    ACCESS_TOKEN_URL = 'https://www.khanacademy.org/api/auth/access_token'
    REDIRECT_URI_PARAMETER_NAME = 'oauth_callback'

    def oauth_authorization_request(self, token):
        """Generate OAuth request to authorize token."""
        key, secret = self.get_key_and_secret()
        state = self.get_or_create_state()
        auth_client = Client(
            key, secret,
            signature_method=SIGNATURE_HMAC,
            signature_type=SIGNATURE_TYPE_QUERY,
            callback_uri=self.get_redirect_uri(state)
        )
        url, headers, body = auth_client.sign(self.REQUEST_TOKEN_URL)
        return url

    def get_unauthorized_token(self):
        return self.strategy.request_data()

    def get_user_details(self, response):
        """Return user details from Facebook account"""
        return {
            'username': response.get('key_email'),
            'email': response.get('key_email'),
            'fullname': '',
            'first_name': '',
            'last_name': '',
            'user_id': response.get('user_id')
        }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json('https://www.khanacademy.org/api/v1/user',
                             auth=self.oauth_auth(access_token))
