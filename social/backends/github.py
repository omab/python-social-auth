"""
GitHub OAuth support.

This contribution adds support for GitHub OAuth service. The settings
GITHUB_APP_ID and GITHUB_API_SECRET must be defined with the values
given by GitHub application registration process.

Extended permissions are supported by defining GITHUB_EXTENDED_PERMISSIONS
setting, it must be a list of values to request.

By default account id and token expiration time are stored in extra_data
field, check OAuthBackend class for details on how to extend it.
"""
from requests import HTTPError

from social.exceptions import AuthFailed
from social.backends.oauth import BaseOAuth2


class GithubOAuth2(BaseOAuth2):
    """Github OAuth authentication backend"""
    name = 'github'
    AUTHORIZATION_URL = 'https://github.com/login/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from Github account"""
        return {'username': response.get('login'),
                'email': response.get('email') or '',
                'first_name': response.get('name')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json('https://api.github.com/user', params={
            'access_token': access_token
        })


class GithubOrganizationOAuth2(GithubOAuth2):
    """Github OAuth2 authentication backend for organizations"""
    name = 'github-org'

    def get_user_details(self, response):
        """Return user details from Github account"""
        return {'username': response.get('login'),
                'email': response.get('email') or '',
                'first_name': response.get('name')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        user_data = super(GithubOrganizationOAuth2, self).user_data(
            access_token, *args, **kwargs
        )
        url = 'https://api.github.com/orgs/{org}/members/{username}'\
                    .format(org=self.setting('NAME'),
                            username=user_data.get('login'))
        try:
            self.request(url, params={'access_token': access_token})
        except HTTPError as err:
            # if the user is a member of the organization, response code
            # will be 204, see http://bit.ly/ZS6vFl
            if err.response.status_code != 204:
                raise AuthFailed('User doesn\'t belong to the organization')
        return user_data
