"""
Github OAuth2 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/github.html
"""
from requests import HTTPError

from six.moves.urllib.parse import urljoin

from social.backends.oauth import BaseOAuth2
from social.exceptions import AuthFailed


class GithubOAuth2(BaseOAuth2):
    """Github OAuth authentication backend"""
    name = 'github'
    AUTHORIZATION_URL_SUFFIX = 'login/oauth/authorize'
    ACCESS_TOKEN_URL_SUFFIX = 'login/oauth/access_token'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires'),
        ('login', 'login')
    ]

    @property
    def API_URL(self):
        return 'https://api.github.com/'

    @property
    def AUTHORIZATION_URL(self):
        return urljoin('https://github.com/', self.AUTHORIZATION_URL_SUFFIX)

    @property
    def ACCESS_TOKEN_URL(self):
        return urljoin('https://github.com/', self.ACCESS_TOKEN_URL_SUFFIX)

    def get_user_details(self, response):
        """Return user details from Github account"""
        fullname, first_name, last_name = self.get_user_names(
            response.get('name')
        )
        return {'username': response.get('login'),
                'email': response.get('email') or '',
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        data = self._user_data(access_token)
        if not data.get('email'):
            try:
                emails = self._user_data(access_token, '/emails')
            except (HTTPError, ValueError, TypeError):
                emails = []

            if emails:
                email = emails[0]
                primary_emails = [e for e in emails
                                    if not isinstance(e, dict) or
                                       e.get('primary')]

                if primary_emails:
                    email = primary_emails[0]
                if isinstance(email, dict):
                    email = email.get('email', '')
                data['email'] = email
        return data

    def _user_data(self, access_token, path=None):
        url = urljoin(self.API_URL, 'user{0}'.format(path or ''))
        return self.get_json(url, params={'access_token': access_token})


class GithubMemberOAuth2(GithubOAuth2):
    no_member_string = ''

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        user_data = super(GithubMemberOAuth2, self).user_data(
            access_token, *args, **kwargs
        )
        try:
            self.request(self.member_url(user_data), params={
                'access_token': access_token
            })
        except HTTPError as err:
            # if the user is a member of the organization, response code
            # will be 204, see http://bit.ly/ZS6vFl
            if err.response.status_code != 204:
                raise AuthFailed(self,
                                 'User doesn\'t belong to the organization')
        return user_data

    def member_url(self, user_data):
        raise NotImplementedError('Implement in subclass')


class GithubOrganizationOAuth2(GithubMemberOAuth2):
    """Github OAuth2 authentication backend for organizations"""
    name = 'github-org'
    no_member_string = 'User doesn\'t belong to the organization'

    def member_url(self, user_data):
        return urljoin(self.API_URL, 'orgs/{org}/members/{username}'.format(
            org=self.setting('NAME'),
            username=user_data.get('login')))


class GithubTeamOAuth2(GithubMemberOAuth2):
    """Github OAuth2 authentication backend for teams"""
    name = 'github-team'
    no_member_string = 'User doesn\'t belong to the team'

    def member_url(self, user_data):
        return urljoin(self.API_URL, 'teams/{team_id}/members/{username}'.format(
            team_id=self.setting('ID'),
            username=user_data.get('login')))
