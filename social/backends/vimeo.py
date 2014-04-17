from social.p3 import urlencode, unquote

from social.backends.oauth import BaseOAuth1, BaseOAuth2


class VimeoOAuth1(BaseOAuth1):
    """Vimeo OAuth authentication backend"""
    name = 'vimeo'
    AUTHORIZATION_URL = 'https://vimeo.com/oauth/authorize'
    REQUEST_TOKEN_URL = 'https://vimeo.com/oauth/request_token'
    ACCESS_TOKEN_URL = 'https://vimeo.com/oauth/access_token'

    def get_user_id(self, details, response):
        return response.get('person', {}).get('id')

    def get_user_details(self, response):
        """Return user details from Twitter account"""
        person = response.get('person', {})
        fullname = person.get('display_name', '')
        if ' ' in fullname:
            first_name, last_name = fullname.split(' ', 1)
        else:
            first_name, last_name = fullname, ''
        return {'username': person.get('username', ''),
                'email': '',
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        return self.get_json(
            'https://vimeo.com/api/rest/v2',
            params={'format': 'json', 'method': 'vimeo.people.getInfo'},
            auth=self.oauth_auth(access_token)
        )


class VimeoOAuth2(BaseOAuth2):
    """Vimeo OAuth2 authentication backend"""
    name = 'vimeo-oauth2'
    AUTHORIZATION_URL = 'https://api.vimeo.com/oauth/authorize'
    ACCESS_TOKEN_URL  = 'https://api.vimeo.com/oauth/access_token'
    REFRESH_TOKEN_URL = 'https://api.vimeo.com/oauth/request_token'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_PARAMETER_NAME = 'scope'
    SCOPE_SEPARATOR = ' '

    API_ACCEPT_HEADER = {'Accept' : 'application/vnd.vimeo.*+json;version=3.0'}

    def get_redirect_uri(self, state=None):
        """
        Build redirect with redirect_state parameter.

        @Vimeo API 3 requires exact redirect uri without additional
        additional state parameter included
        """
        return self.redirect_uri

    def auth_url(self):
        """Return redirect url - scopes require %20 instead of + for space"""
        if self.STATE_PARAMETER or self.REDIRECT_STATE:
            # Store state in session for further request validation. The state
            # value is passed as state parameter (as specified in OAuth2 spec),
            # but also added to redirect, that way we can still verify the
            # request if the provider doesn't implement the state parameter.
            # Reuse token if any.
            name = self.name + '_state'
            state = self.strategy.session_get(name)
            if state is None:
                state = self.state_token()
                self.strategy.session_set(name, state)
        else:
            state = None

        params = self.auth_params(state)
        params.update(self.get_scope_argument())
        params.update(self.auth_extra_arguments())
        params = urlencode(params, doseq=0).replace('+', '%20')
        if not self.REDIRECT_STATE:
            # redirect_uri matching is strictly enforced, so match the
            # providers value exactly.
            params = unquote(params)
        return self.AUTHORIZATION_URL + '?' + params

    def get_user_id(self, details, response):
        """Return user id"""
        try:
            user_id = response.get('user', {})['uri'].split('/')[-1]
        except KeyError:
            user_id = None
        return user_id

    def get_user_details(self, response):
        """Return user details from account"""
        user = response.get('user', {})
        fullname = user.get('name', '')

        if ' ' in fullname:
            first_name, last_name = fullname.split(' ', 1)
        else:
            first_name, last_name = fullname, ''

        return {'username': fullname,
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name,}

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        return self.get_json(
            'https://api.vimeo.com/me',
            params={'access_token' : access_token},
            headers=VimeoOAuth2.API_ACCEPT_HEADER,
        )
