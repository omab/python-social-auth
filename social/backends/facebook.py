"""
Facebook OAuth support.

This contribution adds support for Facebook OAuth service. The settings
SOCIAL_AUHT_FACEBOOK_KEY and SOCIAL_AUTH_FACEBOOK_SECRET must be defined with
the values given by Facebook application registration process.

Extended permissions are supported by defining
SOCIAL_AUTH_FACEBOOK_EXTENDED_PERMISSIONS setting, it must be a list of values
to request.

By default account id and token expiration time are stored in extra_data
field, check OAuthBackend class for details on how to extend it.
"""
import hmac
import time
import json
import base64
import hashlib

from social.utils import parse_qs
from social.backends.oauth import BaseOAuth2
from social.exceptions import AuthException, AuthCanceled, AuthUnknownError


class FacebookOAuth2(BaseOAuth2):
    """Facebook OAuth2 authentication backend"""
    name = 'facebook'
    RESPONSE_TYPE = None
    SCOPE_SEPARATOR = ','
    AUTHORIZATION_URL = 'https://www.facebook.com/dialog/oauth'
    ACCESS_TOKEN_URL = 'https://graph.facebook.com/oauth/access_token'
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from Facebook account"""
        return {'username': response.get('username', response.get('name')),
                'email': response.get('email', ''),
                'fullname': response.get('name', ''),
                'first_name': response.get('first_name', ''),
                'last_name': response.get('last_name', '')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        params = self.setting('PROFILE_EXTRA_PARAMS', {})
        params['access_token'] = access_token
        return self.get_json('https://graph.facebook.com/me',
                             params=params)

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        self.process_error(self.data)
        state = self.validate_state()
        key, secret = self.get_key_and_secret()
        url = self.ACCESS_TOKEN_URL
        response = self.get_querystring(url, params={
            'client_id': key,
            'redirect_uri': self.get_redirect_uri(state),
            'client_secret': secret,
            'code': self.data['code']
        })
        access_token = response['access_token']
        return self.do_auth(access_token, response, *args, **kwargs)

    def process_refresh_token_response(self, response, *args, **kwargs):
        return parse_qs(response.content)

    def refresh_token_params(self, token, *args, **kwargs):
        client_id, client_secret = self.get_key_and_secret()
        return {
            'fb_exchange_token': token,
            'grant_type': 'fb_exchange_token',
            'client_id': client_id,
            'client_secret': client_secret
        }

    def do_auth(self, access_token, response, *args, **kwargs):
        data = self.user_data(access_token)

        if not isinstance(data, dict):
            # From time to time Facebook responds back a JSON with just
            # False as value, the reason is still unknown, but since the
            # data is needed (it contains the user ID used to identify the
            # account on further logins), this app cannot allow it to
            # continue with the auth process.
            raise AuthUnknownError(self, 'An error ocurred while retrieving '
                                         'users Facebook data')

        data['access_token'] = access_token
        if 'expires' in response:
            data['expires'] = response['expires']
        kwargs.update({'backend': self, 'response': data})
        return self.strategy.authenticate(*args, **kwargs)


class FacebookAppOAuth2(FacebookOAuth2):
    """Facebook Application Authentication support"""
    name = 'facebook-app'

    def uses_redirect(self):
        return False

    def auth_complete(self, *args, **kwargs):
        access_token = None
        response = {}

        if 'signed_request' in self.data:
            key, secret = self.get_key_and_secret()
            response = self.load_signed_request(self.data['signed_request'])
            if not 'user_id' in response and not 'oauth_token' in response:
                raise AuthException(self)

            if response is not None:
                access_token = response.get('access_token') or \
                               response['oauth_token'] or \
                               self.data.get('access_token')

        if access_token is None:
            if self.data.get('error') == 'access_denied':
                raise AuthCanceled(self)
            else:
                raise AuthException(self)
        return self.do_auth(access_token, response, *args, **kwargs)

    def auth_html(self):
        key, secret = self.get_key_and_secret()
        namespace = self.setting('NAMESPACE', None)
        scope = self.setting('SCOPE', '')
        if scope:
            scope = self.SCOPE_SEPARATOR.join(scope)
        ctx = {
            'FACEBOOK_APP_NAMESPACE': namespace or key,
            'FACEBOOK_KEY': key,
            'FACEBOOK_EXTENDED_PERMISSIONS': scope,
            'FACEBOOK_COMPLETE_URI': self.redirect_uri,
        }
        html = self.setting('LOCAL_HTML', 'facebook.html')
        return self.strategy.render_html(html, ctx)

    def load_signed_request(self, signed_request):
        def base64_url_decode(data):
            data = data.encode('ascii')
            data += '=' * (4 - (len(data) % 4))
            return base64.urlsafe_b64decode(data)

        key, secret = self.get_key_and_secret()
        try:
            sig, payload = signed_request.split('.', 1)
        except ValueError:
            pass  # ignore if can't split on dot
        else:
            sig = base64_url_decode(sig)
            data = json.loads(base64_url_decode(payload))
            expected_sig = hmac.new(secret, msg=payload,
                                    digestmod=hashlib.sha256).digest()
            # allow the signed_request to function for upto 1 day
            if sig == expected_sig and \
               data['issued_at'] > (time.time() - 86400):
                return data
