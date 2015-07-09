"""
Github Enterprise OAuth2 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/github_enterprise.html
"""
from six.moves.urllib.parse import urljoin

from social.backends.github import (
    GithubOAuth2, GithubOrganizationOAuth2, GithubTeamOAuth2)


def append_slash(url):
    """Make sure we append a slash at the end of the URL otherwise we have issues with urljoin
    Example:
    >>> urlparse.urljoin('http://www.example.com/api/v3', 'user/1/')
    'http://www.example.com/api/user/1/'
    """
    if not url:
        return url
    return "%s/" % url if not url.endswith('/') else url


class GithubEnterpriseMixin(object):

    @property
    def API_URL(self):
        return append_slash(self.setting('API_URL'))

    @property
    def AUTHORIZATION_URL(self):
        return urljoin(append_slash(self.setting('URL')), GithubOAuth2.AUTHORIZATION_URL_SUFFIX)

    @property
    def ACCESS_TOKEN_URL(self):
        return urljoin(append_slash(self.setting('URL')), GithubOAuth2.ACCESS_TOKEN_URL_SUFFIX)


class GithubEnterpriseOAuth2(GithubEnterpriseMixin, GithubOAuth2):
    """Github Enterprise OAuth authentication backend"""
    name = 'github-enterprise'


class GithubEnterpriseOrganizationOAuth2(GithubEnterpriseMixin, GithubOrganizationOAuth2):
    """Github Enterprise OAuth2 authentication backend for organizations"""
    DEFAULT_SCOPE = ['read:org']
    name = 'github-enterprise-org'


class GithubEnterpriseTeamOAuth2(GithubEnterpriseMixin, GithubTeamOAuth2):
    """Github Enterprise OAuth2 authentication backend for teams"""
    DEFAULT_SCOPE = ['read:org']
    name = 'github-enterprise-team'
