import sys
import json

sys.path.insert(0, '..')

from social.backends.github import GithubOAuth2
from tests.oauth2_tests import OAuth2Test


class GithubTest(OAuth2Test):
    backend = GithubOAuth2
    complete_url = '/complete/github/?code=foobar'
    user_data_url = 'https://api.github.com/user'
    access_token_body = json.dumps({
        'access_token': 'foobar',
        'token_type': 'bearer'
    })
    user_data_body = json.dumps({
        'login': 'octocat',
        'id': 1,
        'avatar_url': 'https://github.com/images/error/octocat_happy.gif',
        'gravatar_id': 'somehexcode',
        'url': 'https://api.github.com/users/octocat',
        'name': 'monalisa octocat',
        'company': 'GitHub',
        'blog': 'https://github.com/blog',
        'location': 'San Francisco',
        'email': 'octocat@github.com',
        'hireable': False,
        'bio': 'There once was...',
        'public_repos': 2,
        'public_gists': 1,
        'followers': 20,
        'following': 0,
        'html_url': 'https://github.com/octocat',
        'created_at': '2008-01-14T04:33:35Z',
        'type': 'User',
        'total_private_repos': 100,
        'owned_private_repos': 100,
        'private_gists': 81,
        'disk_usage': 10000,
        'collaborators': 8,
        'plan': {
            'name': 'Medium',
            'space': 400,
            'collaborators': 10,
            'private_repos': 20
        }
    })
    settings = {
        'SOCIAL_AUTH_GITHUB_KEY': 'a-key',
        'SOCIAL_AUTH_GITHUB_SECRET': 'a-secret-key'
    }
    expected_username = 'octocat'

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()
