"""
Linkedin OAuth support

No extra configurations are needed to make this work.
"""
from social.backends.oauth import BaseOAuth1, BaseOAuth2


class BaseLinkedinAuth(object):
    EXTRA_DATA = [('id', 'id'),
                  ('first-name', 'first_name'),
                  ('last-name', 'last_name')]
    USER_DETAILS = 'https://api.linkedin.com/v1/people/~:(%s)'

    def get_user_details(self, response):
        """Return user details from Linkedin account"""
        first_name = response['firstName']
        last_name = response['lastName']
        email = response.get('emailAddress', '')
        return {'username': first_name + last_name,
                'fullname': first_name + ' ' + last_name,
                'first_name': first_name,
                'last_name': last_name,
                'email': email}

    def user_details_url(self):
        # use set() since LinkedIn fails when values are duplicated
        fields_selectors = list(set(['first-name', 'id', 'last-name'] +
                                self.setting('FIELD_SELECTORS', [])))
        # user sort to ease the tests URL mocking
        fields_selectors.sort()
        fields_selectors = ','.join(fields_selectors)
        return self.USER_DETAILS % fields_selectors


class LinkedinOAuth(BaseLinkedinAuth, BaseOAuth1):
    """Linkedin OAuth authentication backend"""
    name = 'linkedin'
    SCOPE_SEPARATOR = '+'
    AUTHORIZATION_URL = 'https://www.linkedin.com/uas/oauth/authenticate'
    REQUEST_TOKEN_URL = 'https://api.linkedin.com/uas/oauth/requestToken'
    ACCESS_TOKEN_URL = 'https://api.linkedin.com/uas/oauth/accessToken'

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        return self.get_json(
            self.user_details_url(),
            params={'format': 'json'},
            auth=self.oauth_auth(access_token)
        )

    def unauthorized_token(self):
        """Makes first request to oauth. Returns an unauthorized Token."""
        scope = self.get_scope() or ''
        if scope:
            scope = '?scope=' + self.SCOPE_SEPARATOR.join(scope)
        return self.request(self.REQUEST_TOKEN_URL + scope,
                            params=self.request_token_extra_arguments(),
                            auth=self.oauth_auth()).content


class LinkedinOAuth2(BaseLinkedinAuth, BaseOAuth2):
    name = 'linkedin-oauth2'
    SCOPE_SEPARATOR = ' '
    AUTHORIZATION_URL = 'https://www.linkedin.com/uas/oauth2/authorization'
    ACCESS_TOKEN_URL = 'https://www.linkedin.com/uas/oauth2/accessToken'
    ACCESS_TOKEN_METHOD = 'POST'

    def user_data(self, access_token, *args, **kwargs):
        return self.get_json(self.user_details_url(), params={
            'oauth2_access_token': access_token,
            'format': 'json'
        })
