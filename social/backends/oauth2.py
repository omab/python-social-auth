import json
from urllib2 import Request, HTTPError
from urllib import urlencode

from social.utils import url_add_parameters, dsa_urlopen
from social.exceptions import AuthFailed, AuthCanceled, AuthUnknownError, \
                              AuthMissingParameter, AuthStateMissing, \
                              AuthStateForbidden
from social.backends.oauth import OAuthAuth


class BaseOAuth2(OAuthAuth):
    """Base class for OAuth2 providers.

    OAuth2 draft details at:
        http://tools.ietf.org/html/draft-ietf-oauth-v2-10

    Attributes:
        AUTHORIZATION_URL       Authorization service url
        ACCESS_TOKEN_URL        Token URL
    """
    AUTHORIZATION_URL = None
    ACCESS_TOKEN_URL = None
    REFRESH_TOKEN_URL = None
    RESPONSE_TYPE = 'code'
    REDIRECT_STATE = True
    STATE_PARAMETER = True

    def state_token(self):
        """Generate csrf token to include as state parameter."""
        return self.strategy.random_string(32)

    def get_redirect_uri(self, state=None):
        """Build redirect with redirect_state parameter."""
        uri = self.redirect
        if self.REDIRECT_STATE and state:
            uri = url_add_parameters(uri, {'redirect_state': state})
        return uri

    def auth_params(self, state=None):
        client_id, client_secret = self.get_key_and_secret()
        params = {
            'client_id': client_id,
            'redirect_uri': self.get_redirect_uri(state)
        }
        if self.STATE_PARAMETER and state:
            params['state'] = state
        if self.RESPONSE_TYPE:
            params['response_type'] = self.RESPONSE_TYPE
        return params

    def auth_url(self):
        """Return redirect url"""
        if self.STATE_PARAMETER or self.REDIRECT_STATE:
            # Store state in session for further request validation. The state
            # value is passed as state parameter (as specified in OAuth2 spec),
            # but also added to redirect, that way we can still verify the
            # request if the provider doesn't implement the state parameter.
            # Reuse token if any.
            name = self.titled_name + '_state'
            state = self.strategy.session_get(name)
            if state is None:
                state = self.state_token()
                self.strategy.session_set(name, state)
        else:
            state = None

        params = self.auth_params(state)
        params.update(self.get_scope_argument())
        params.update(self.auth_extra_arguments())
        query_string = self.strategy.request_query_string(self)
        if query_string:
            query_string = '&' + query_string
        return self.AUTHORIZATION_URL + '?' + urlencode(params) + query_string

    def validate_state(self):
        """Validate state value. Raises exception on error, returns state
        value if valid."""
        if not self.STATE_PARAMETER and not self.REDIRECT_STATE:
            return None
        state = self.strategy.session_get(self.titled_name + '_state')
        if state:
            request_state = self.data.get('state') or \
                            self.data.get('redirect_state')
            if not request_state:
                raise AuthMissingParameter(self, 'state')
            elif not state:
                raise AuthStateMissing(self, 'state')
            elif not request_state == state:
                raise AuthStateForbidden(self)
        return state

    def process_error(self, data):
        if data.get('error'):
            raise AuthFailed(self, self.data.get('error_description') or
                                   self.data['error'])

    def auth_complete_params(self, state=None):
        client_id, client_secret = self.get_key_and_secret()
        return {
            'grant_type': 'authorization_code',  # request auth code
            'code': self.data.get('code', ''),  # server response code
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': self.get_redirect_uri(state)
        }

    def auth_headers(self):
        return {'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'}

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        self.process_error(self.data)
        params = self.auth_complete_params(self.validate_state())
        request = Request(self.ACCESS_TOKEN_URL, data=urlencode(params),
                          headers=self.auth_headers())

        try:
            response = json.loads(dsa_urlopen(request).read())
        except HTTPError, e:
            if e.code == 400:
                raise AuthCanceled(self)
            else:
                raise
        except (ValueError, KeyError):
            raise AuthUnknownError(self)

        self.process_error(response)
        return self.do_auth(response['access_token'], response=response,
                            *args, **kwargs)

    def refresh_token_params(self, token):
        client_id, client_secret = self.get_key_and_secret()
        return {
            'refresh_token': token,
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'client_secret': client_secret
        }

    def process_refresh_token_response(self, response):
        return json.loads(response)

    def refresh_token(self, token):
        request = Request(
            self.REFRESH_TOKEN_URL or self.ACCESS_TOKEN_URL,
            data=urlencode(self.refresh_token_params(token)),
            headers=self.auth_headers()
        )
        return self.process_refresh_token_response(
            dsa_urlopen(request).read()
        )

    def do_auth(self, access_token, *args, **kwargs):
        """Finish the auth process once the access_token was retrieved"""
        data = self.user_data(access_token, *args, **kwargs)
        response = kwargs.get('response') or {}
        response.update(data or {})
        kwargs.update({'response': response, self.name: True})
        return self.authenticate(*args, **kwargs)
