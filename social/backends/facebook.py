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
import cgi
import hmac
import time
import json
import base64
import hashlib
from urllib import urlencode
from urllib2 import HTTPError

from social.backends.oauth import BaseOAuth2
from social.exceptions import AuthException, AuthCanceled, AuthFailed, \
                              AuthTokenError, AuthUnknownError


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
        url = 'https://graph.facebook.com/me?' + urlencode(params)
        try:
            return json.load(self.urlopen(url))
        except ValueError:
            return None
        except HTTPError:
            raise AuthTokenError(self)

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        if 'code' in self.data:
            state = self.validate_state()
            key, secret = self.get_key_and_secret()
            url = self.ACCESS_TOKEN_URL + '?' + urlencode({
                'client_id': key,
                'redirect_uri': self.get_redirect_uri(state),
                'client_secret': secret,
                'code': self.data['code']
            })
            try:
                response = cgi.parse_qs(self.urlopen(url).read())
            except HTTPError:
                raise AuthFailed(self, 'There was an error authenticating the'
                                       'the app')

            access_token = response['access_token'][0]
            expires = 'expires' in response and response['expires'][0] or None
            return self.do_auth(access_token, expires=expires, *args, **kwargs)
        else:
            if self.data.get('error') == 'access_denied':
                raise AuthCanceled(self)
            else:
                raise AuthException(self)

    @classmethod
    def process_refresh_token_response(cls, response):
        return dict((key, val[0])
                        for key, val in cgi.parse_qs(response).iteritems())

    @classmethod
    def refresh_token_params(cls, token):
        client_id, client_secret = cls.get_key_and_secret()
        return {
            'fb_exchange_token': token,
            'grant_type': 'fb_exchange_token',
            'client_id': client_id,
            'client_secret': client_secret
        }

    def do_auth(self, access_token, expires=None, *args, **kwargs):
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
        if expires:  # expires is None on offline access
            data['expires'] = expires

        kwargs.update({'backend': self, 'response': data})
        return self.strategy.authenticate(*args, **kwargs)

    def load_signed_request(self, signed_request):
        def base64_url_decode(data):
            data = data.encode(u'ascii')
            data += '=' * (4 - (len(data) % 4))
            return base64.urlsafe_b64decode(data)

        key, secret = self.get_key_and_secret()
        try:
            sig, payload = signed_request.split(u'.', 1)
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


class FacebookAppOAuth2(FacebookOAuth2):
    """Facebook Application Authentication support"""
    name = 'facebook-app'

    def uses_redirect(self):
        return False

    def auth_complete(self, *args, **kwargs):
        access_token = None
        expires = None

        if 'signed_request' in self.data:
            key, secret = self.get_key_and_secret()
            response = self.load_signed_request(self.data['signed_request'])
            if not 'user_id' in response and not 'oauth_token' in response:
                raise AuthException(self)

            if response is not None:
                access_token = response.get('access_token') or \
                               response['oauth_token'] or \
                               self.data.get('access_token')
                if 'expires' in response:
                    expires = response['expires']

        if access_token is None:
            if self.data.get('error') == 'access_denied':
                raise AuthCanceled(self)
            else:
                raise AuthException(self)
        return self.do_auth(access_token, expires=expires, *args, **kwargs)

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
