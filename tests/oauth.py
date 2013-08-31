import requests

from sure import expect
from httpretty import HTTPretty

from social.p3 import urlparse
from social.utils import parse_qs, module_member
from social.backends.utils import load_backends

from tests.base import BaseBackendTest
from tests.models import TestStorage, User, TestUserSocialAuth, TestNonce, \
                         TestAssociation
from tests.strategy import TestStrategy


class BaseOAuthTest(BaseBackendTest):
    backend = None
    backend_path = None
    user_data_body = None
    user_data_url = ''
    user_data_content_type = 'application/json'
    access_token_body = None
    access_token_status = 200
    expected_username = ''
    raw_complete_url = ''

    def setUp(self):
        HTTPretty.enable()
        self.backend = module_member(self.backend_path)
        name = self.backend.name
        self.complete_url = self.raw_complete_url.format(name)
        self.strategy = TestStrategy(self.backend, TestStorage)
        name = name.upper().replace('-', '_')
        self.strategy.set_settings({
            'SOCIAL_AUTH_' + name + '_KEY': 'a-key',
            'SOCIAL_AUTH_' + name + '_SECRET': 'a-secret-key',
            'SOCIAL_AUTH_AUTHENTICATION_BACKENDS': (
                self.backend_path,
                'tests.backends.broken_test.BrokenBackendAuth'
            )
        })
        # Force backends loading to trash PSA cache
        load_backends(
            self.strategy.get_setting('SOCIAL_AUTH_AUTHENTICATION_BACKENDS'),
            force_load=True
        )

    def tearDown(self):
        self.strategy = None
        self.complete_url = None
        self.backend = None
        User.reset_cache()
        TestUserSocialAuth.reset_cache()
        TestNonce.reset_cache()
        TestAssociation.reset_cache()
        HTTPretty.disable()

    def _method(self, method):
        return {'GET': HTTPretty.GET,
                'POST': HTTPretty.POST}[method]

    def handle_state(self, start_url, target_url):
        try:
            if self.backend.STATE_PARAMETER or self.backend.REDIRECT_STATE:
                query = parse_qs(urlparse(start_url).query)
                target_url = target_url + ('?' in target_url and '&' or '?')
                if 'state' in query or 'redirect_state' in query:
                    name = 'state' in query and 'state' or 'redirect_state'
                    target_url += '{0}={1}'.format(name, query[name])
        except AttributeError:
            pass
        return target_url

    def auth_handlers(self, start_url):
        target_url = self.handle_state(start_url,
                                       self.strategy.build_absolute_uri(
                                           self.complete_url
                                       ))
        HTTPretty.register_uri(HTTPretty.GET,
                               start_url,
                               status=301,
                               location=target_url)
        HTTPretty.register_uri(HTTPretty.GET,
                               target_url,
                               status=200,
                               body='foobar')
        HTTPretty.register_uri(self._method(self.backend.ACCESS_TOKEN_METHOD),
                               uri=self.backend.ACCESS_TOKEN_URL,
                               status=self.access_token_status,
                               body=self.access_token_body or '',
                               content_type='text/json')
        if self.user_data_url:
            HTTPretty.register_uri(HTTPretty.GET,
                                   self.user_data_url,
                                   body=self.user_data_body or '',
                                   content_type=self.user_data_content_type)
        return target_url

    def do_start(self):
        start_url = self.strategy.start().url
        target_url = self.auth_handlers(start_url)
        response = requests.get(start_url)
        expect(response.url).to.equal(target_url)
        expect(response.text).to.equal('foobar')
        self.strategy.set_request_data(parse_qs(urlparse(target_url).query))
        return self.strategy.complete()


class OAuth1Test(BaseOAuthTest):
    request_token_body = None
    raw_complete_url = '/complete/{0}/?oauth_verifier=bazqux&' \
                                      'oauth_token=foobar'

    def request_token_handler(self):
        HTTPretty.register_uri(self._method(self.backend.REQUEST_TOKEN_METHOD),
                               self.backend.REQUEST_TOKEN_URL,
                               body=self.request_token_body,
                               status=200)

    def do_start(self):
        self.request_token_handler()
        return super(OAuth1Test, self).do_start()


class OAuth2Test(BaseOAuthTest):
    raw_complete_url = '/complete/{0}/?code=foobar'
    refresh_token_body = ''

    def refresh_token_arguments(self):
        return {}

    def do_refresh_token(self):
        self.do_login()
        HTTPretty.register_uri(self._method(self.backend.REFRESH_TOKEN_METHOD),
                               self.backend.REFRESH_TOKEN_URL or
                               self.backend.ACCESS_TOKEN_URL,
                               status=200,
                               body=self.refresh_token_body)
        user = list(User.cache.values())[0]
        social = user.social[0]
        social.refresh_token(strategy=self.strategy,
                             **self.refresh_token_arguments())
        return user, social
