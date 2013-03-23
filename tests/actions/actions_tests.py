import json
import requests
import unittest

from sure import expect
from httpretty import HTTPretty

from social.utils import parse_qs, module_member
from social.p3 import urlparse
from social.actions import do_auth, do_complete

from tests.models import TestStorage, User, TestUserSocialAuth, TestNonce, \
                         TestAssociation
from tests.strategy import TestStrategy


class BaseActionTest(unittest.TestCase):
    user_data_url = 'https://api.github.com/user'
    login_redirect_url = '/success'
    expected_username = 'octocat'
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

    def setUp(self):
        HTTPretty.enable()
        User.reset_cache()
        TestUserSocialAuth.reset_cache()
        TestNonce.reset_cache()
        TestAssociation.reset_cache()
        self.backend = module_member('social.backends.github.GithubOAuth2')
        self.strategy = TestStrategy(self.backend, TestStorage)
        self.user = None

    def tearDown(self):
        self.backend = None
        self.strategy = None
        self.user = None
        User.reset_cache()
        TestUserSocialAuth.reset_cache()
        TestNonce.reset_cache()
        TestAssociation.reset_cache()
        HTTPretty.disable()

    def do_login(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_GITHUB_KEY': 'a-key',
            'SOCIAL_AUTH_GITHUB_SECRET': 'a-secret-key',
            'SOCIAL_AUTH_LOGIN_REDIRECT_URL': self.login_redirect_url,
            'SOCIAL_AUTH_AUTHENTICATION_BACKENDS': (
                'social.backends.github.GithubOAuth2',
            )
        })
        start_url = do_auth(self.strategy).url
        target_url = self.strategy.build_absolute_uri(
            '/complete/github/?code=foobar'
        )

        start_query = parse_qs(urlparse(start_url).query)
        location_url = target_url + ('?' in target_url and '&' or '?') + \
                       'state=' + start_query['state']
        location_query = parse_qs(urlparse(location_url).query)

        HTTPretty.register_uri(HTTPretty.GET, start_url, status=301,
                               location=location_url)
        HTTPretty.register_uri(HTTPretty.GET, location_url, status=200,
                               body='foobar')

        response = requests.get(start_url)
        expect(response.url).to.equal(location_url)
        expect(response.text).to.equal('foobar')

        HTTPretty.register_uri(HTTPretty.GET,
                               uri=self.backend.ACCESS_TOKEN_URL,
                               status=200,
                               body=self.access_token_body or '',
                               content_type='text/json')

        if self.user_data_url:
            HTTPretty.register_uri(HTTPretty.GET, self.user_data_url,
                                   body=self.user_data_body or '',
                                   content_type='text/json')
        self.strategy.set_request_data(location_query)
        out_url = do_complete(
            self.strategy,
            user=self.user,
            login=lambda strategy, user: strategy.session_set('username',
                                                              user.username)
        )
        expect(self.strategy.session_get('username')).to.equal(
            self.expected_username
        )
        expect(out_url.url).to.equal(self.login_redirect_url)
