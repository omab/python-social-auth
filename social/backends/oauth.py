from urllib2 import HTTPError

from oauth2 import Token, Request as OAuthRequest, Consumer as OAuthConsumer

from social.utils import dsa_urlopen
from social.exceptions import AuthCanceled, AuthTokenError
from social.utils import build_consumer_oauth_request
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
    SETTINGS_KEY_NAME = ''
    SETTINGS_SECRET_NAME = ''
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
        return self.strategy.setting(self.SETTINGS_KEY_NAME), \
               self.strategy.setting(self.SETTINGS_SECRET_NAME)

    def enabled(self):
        """Return backend enabled status by checking basic settings"""
        return self.strategy.setting(self.SETTINGS_KEY_NAME) and \
               self.strategy.setting(self.SETTINGS_SECRET_NAME)

    def get_scope(self):
        """Return list with needed access scope"""
        scope = self.DEFAULT_SCOPE or []
        if self.SCOPE_VAR_NAME:
            scope = scope + self.strategy.setting(self.SCOPE_VAR_NAME, [])
        return scope

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
        kwargs.update({'response': data, self.name: True})
        return self.authenticate(*args, **kwargs)

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
            callback=self.redirect,
            http_url=self.AUTHORIZATION_URL,
            parameters=params
        )

    def oauth_request(self, token, url, extra_params=None):
        """Generate OAuth request, setups callback url"""
        return build_consumer_oauth_request(self, token, url,
                                            self.redirect,
                                            self.data.get('oauth_verifier'),
                                            extra_params)

    def fetch_response(self, request):
        """Executes request and fetchs service response"""
        response = dsa_urlopen(request.to_url())
        return '\n'.join(response.readlines())

    def access_token(self, token):
        """Return request for access token value"""
        request = self.oauth_request(token, self.ACCESS_TOKEN_URL)
        return Token.from_string(self.fetch_response(request))

    @property
    def consumer(self):
        """Setups consumer"""
        return OAuthConsumer(*self.get_key_and_secret())
