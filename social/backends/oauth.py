import json
from urllib2 import Request, HTTPError
from urllib import urlencode

from oauth2 import Token, SignatureMethod_HMAC_SHA1, HTTP_METHOD, \
                   Request as OAuthRequest, Consumer as OAuthConsumer

from social.utils import url_add_parameters
from social.exceptions import AuthFailed, AuthCanceled, AuthUnknownError, \
                              AuthMissingParameter, AuthStateMissing, \
                              AuthStateForbidden, AuthTokenError
from social.backends.base import BaseAuth


class OAuthAuth(BaseAuth):
    """OAuth authentication backend base class.

    EXTRA_DATA defines a set of name that will be stored in
               extra_data field. It must be a list of tuples with
               name and alias.

    Also settings will be inspected to get more values names that should be
    stored on extra_data field. Setting name is created from current backend
    name (all uppercase) plus _EXTRA_DATA.

    access_token is always stored.
    """
    SCOPE_VAR_NAME = None
    SCOPE_PARAMETER_NAME = 'scope'
    DEFAULT_SCOPE = None
    SCOPE_SEPARATOR = ' '
    EXTRA_DATA = None
    ID_KEY = 'id'

    def get_user_id(self, details, response):
        """OAuth providers return an unique user id in response"""
        return response[self.ID_KEY]

    def extra_data(self, user, uid, response, details=None):
        """Return access_token and extra defined names to store in
        extra_data field"""
        data = {'access_token': response.get('access_token', '')}
        names = (self.EXTRA_DATA or []) + \
                self.strategy.setting('EXTRA_DATA', [])
        for entry in names:
            if len(entry) == 2:
                (name, alias), discard = entry, False
            elif len(entry) == 3:
                name, alias, discard = entry
            elif len(entry) == 1:
                name = alias = entry
            else:  # ???
                continue

            value = response.get(name)
            if discard and not value:
                continue
            data[alias] = value
        return data

    def get_key_and_secret(self):
        """Return tuple with Consumer Key and Consumer Secret for current
        service provider. Must return (key, secret), order *must* be respected.
        """
        return self.strategy.setting(self.titled_name + '_KEY'), \
               self.strategy.setting(self.titled_name + '_SECRET')

    def get_scope(self):
        """Return list with needed access scope"""
        return (self.DEFAULT_SCOPE or []) + \
               self.strategy.setting('SCOPE', [])

    def get_scope_argument(self):
        param = {}
        scope = self.get_scope()
        if scope:
            param[self.SCOPE_PARAMETER_NAME] = self.SCOPE_SEPARATOR.join(scope)
        return param

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service. Implement in subclass"""
        return {}


class ConsumerBasedOAuth(OAuthAuth):
    """Consumer based mechanism OAuth authentication, fill the needed
    parameters to communicate properly with authentication service.

        AUTHORIZATION_URL       Authorization service url
        REQUEST_TOKEN_URL       Request token URL
        ACCESS_TOKEN_URL        Access token URL
    """
    AUTHORIZATION_URL = ''
    REQUEST_TOKEN_URL = ''
    ACCESS_TOKEN_URL = ''

    def auth_url(self):
        """Return redirect url"""
        token = self.unauthorized_token()
        name = self.name + 'unauthorized_token_name'
        tokens = self.strategy.session_get(name, [])
        tokens.append(token.to_string())
        self.strategy.session_set(name, tokens)
        return self.oauth_authorization_request(token).to_url()

    def auth_complete(self, *args, **kwargs):
        """Return user, might be logged in"""
        # Multiple unauthorized tokens are supported (see #521)
        name = self.name + 'unauthorized_token_name'
        token = None
        unauthed_tokens = self.strategy.session_get(name, [])
        if not unauthed_tokens:
            raise AuthTokenError(self, 'Missing unauthorized token')
        for unauthed_token in unauthed_tokens:
            token = Token.from_string(unauthed_token)
            if token.key == self.data.get('oauth_token', 'no-token'):
                self.strategy.session_set(name, list(set(unauthed_tokens) - \
                                                     set([unauthed_token])))
                break
        else:
            raise AuthTokenError(self, 'Incorrect tokens')

        try:
            access_token = self.access_token(token)
        except HTTPError, e:
            if e.code == 400:
                raise AuthCanceled(self)
            else:
                raise
        return self.do_auth(access_token, *args, **kwargs)

    def do_auth(self, access_token, *args, **kwargs):
        """Finish the auth process once the access_token was retrieved"""
        data = self.user_data(access_token)
        if data is not None:
            data['access_token'] = access_token.to_string()
        kwargs.update({'response': data, 'backend': self})
        return self.strategy.authenticate(*args, **kwargs)

    def unauthorized_token(self):
        """Return request for unauthorized token (first stage)"""
        request = self.oauth_request(
            token=None,
            url=self.REQUEST_TOKEN_URL,
            extra_params=self.request_token_extra_arguments()
        )
        return Token.from_string(self.fetch_response(request))

    def oauth_authorization_request(self, token):
        """Generate OAuth request to authorize token."""
        params = self.auth_extra_arguments() or {}
        params.update(self.get_scope_argument())
        return OAuthRequest.from_token_and_callback(
            token=token,
            callback=self.redirect_uri,
            http_url=self.AUTHORIZATION_URL,
            parameters=params
        )

    def oauth_request(self, token, url, extra_params=None):
        """Generate OAuth request, setups callback url"""
        return build_consumer_oauth_request(self, token, url,
                                            self.redirect_uri,
                                            self.data.get('oauth_verifier'),
                                            extra_params)

    def fetch_response(self, request):
        """Executes request and fetchs service response"""
        response = self.urlopen(request.to_url())
        return '\n'.join(response.readlines())

    def access_token(self, token):
        """Return request for access token value"""
        request = self.oauth_request(token, self.ACCESS_TOKEN_URL)
        return Token.from_string(self.fetch_response(request))

    @property
    def consumer(self):
        """Setups consumer"""
        return OAuthConsumer(*self.get_key_and_secret())


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
        uri = self.redirect_uri
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
        query_string = self.strategy.request_query_string()
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
            response = json.loads(self.urlopen(request).read())
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

    def do_auth(self, access_token, *args, **kwargs):
        """Finish the auth process once the access_token was retrieved"""
        data = self.user_data(access_token, *args, **kwargs)
        response = kwargs.get('response') or {}
        response.update(data or {})
        kwargs.update({'response': response, 'backend': self})
        return self.strategy.authenticate(*args, **kwargs)

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
            self.urlopen(request).read()
        )


def build_consumer_oauth_request(backend, token, url, redirect_uri='/',
                                 oauth_verifier=None, extra_params=None,
                                 method=HTTP_METHOD):
    """Builds a Consumer OAuth request."""
    params = {'oauth_callback': redirect_uri}
    if extra_params:
        params.update(extra_params)

    if oauth_verifier:
        params['oauth_verifier'] = oauth_verifier

    consumer = OAuthConsumer(*backend.get_key_and_secret())
    request = OAuthRequest.from_consumer_and_token(consumer,
                                                   token=token,
                                                   http_method=method,
                                                   http_url=url,
                                                   parameters=params)
    request.sign_request(SignatureMethod_HMAC_SHA1(), consumer, token)
    return request
