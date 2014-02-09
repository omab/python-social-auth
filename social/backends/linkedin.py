"""
LinkedIn OAuth1 and OAuth2 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/linkedin.html
"""
from social.backends.oauth import BaseOAuth1, BaseOAuth2


class BaseLinkedinAuth(object):
    EXTRA_DATA = [('id', 'id'),
                  ('first-name', 'first_name', True),
                  ('last-name', 'last_name', True),
                  ('firstName', 'first_name', True),
                  ('lastName', 'last_name', True)]
    USER_DETAILS = 'https://api.linkedin.com/v1/people/~:({0})'

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
        return self.USER_DETAILS.format(fields_selectors)

    def user_data_headers(self):
        lang = self.setting('FORCE_PROFILE_LANGUAGE')
        if lang:
            return {
                'Accept-Language': lang if lang is not True
                                        else self.strategy.get_language()
            }


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
            auth=self.oauth_auth(access_token),
            headers=self.user_data_headers()
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
        return self.get_json(
            self.user_details_url(),
            params={'oauth2_access_token': access_token,
                    'format': 'json'},
            headers=self.user_data_headers()
        )

    def request_access_token(self, *args, **kwargs):
        # LinkedIn expects a POST request with querystring parameters, despite
        # the spec http://tools.ietf.org/html/rfc6749#section-4.1.3
        kwargs['params'] = kwargs.pop('data')
        return super(LinkedinOAuth2, self).request_access_token(
            *args, **kwargs
        )
