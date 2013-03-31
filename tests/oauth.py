import requests
import unittest

from sure import expect
from httpretty import HTTPretty

from social.p3 import urlparse
from social.utils import parse_qs, module_member
from social.backends.utils import user_backends_data, load_backends

from tests.models import TestStorage, User, TestUserSocialAuth, TestNonce, \
                         TestAssociation
from tests.strategy import TestStrategy


class BaseOAuthTest(unittest.TestCase):
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

    def do_login(self):
        user = self.do_start()
        username = self.expected_username
        expect(user.username).to.equal(username)
        expect(self.strategy.session_get('username')).to.equal(username)
        expect(self.strategy.get_user(user.id)).to.equal(user)
        expect(self.strategy.backend.get_user(user.id)).to.equal(user)
        user_backends = user_backends_data(
            user,
            self.strategy.get_setting('SOCIAL_AUTH_AUTHENTICATION_BACKENDS'),
            self.strategy.storage
        )
        expect(len(list(user_backends.keys()))).to.equal(3)
        expect('associated' in user_backends).to.equal(True)
        expect('not_associated' in user_backends).to.equal(True)
        expect('backends' in user_backends).to.equal(True)
        expect(len(user_backends['associated'])).to.equal(1)
        expect(len(user_backends['not_associated'])).to.equal(1)
        expect(len(user_backends['backends'])).to.equal(2)
        return user

    def pipeline_settings(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_PIPELINE': (
                'social.pipeline.partial.save_status_to_session',
                'tests.pipeline.ask_for_password',
                'social.pipeline.social_auth.social_user',
                'social.pipeline.user.get_username',
                'social.pipeline.user.create_user',
                'social.pipeline.social_auth.associate_user',
                'social.pipeline.social_auth.load_extra_data',
                'tests.pipeline.set_password',
                'social.pipeline.user.user_details'
            )
        })

    def pipeline_handlers(self, url):
        HTTPretty.register_uri(HTTPretty.GET, url, status=200, body='foobar')
        HTTPretty.register_uri(HTTPretty.POST, url, status=200)

    def pipeline_password_handling(self, url):
        password = 'foobar'
        requests.get(url)
        requests.post(url, data={'password': password})

        data = parse_qs(HTTPretty.last_request.body)
        expect(data['password']).to.equal(password)
        self.strategy.session_set('password', data['password'])
        return password

    def do_partial_pipeline(self):
        url = self.strategy.build_absolute_uri('/password')
        self.pipeline_settings()
        redirect = self.do_start()
        expect(redirect.url).to.equal(url)
        self.pipeline_handlers(url)
        password = self.pipeline_password_handling(url)

        data = self.strategy.session_pop('partial_pipeline')
        idx, backend, xargs, xkwargs = self.strategy.from_session(data)
        expect(backend).to.equal(self.backend.name)
        user = self.strategy.continue_pipeline(pipeline_index=idx,
                                               *xargs, **xkwargs)

        expect(user.username).to.equal(self.expected_username)
        expect(user.password).to.equal(password)
        return user


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
