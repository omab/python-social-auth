import sys
import requests
import unittest

from sure import expect
from httpretty import HTTPretty

sys.path.insert(0, '..')

from social.utils import parse_qs, module_member
from social.p3 import urlparse

from tests.models import TestStorage, User, TestUserSocialAuth, TestNonce, \
                         TestAssociation
from tests.strategy import TestStrategy


class OAuth1Test(unittest.TestCase):
    backend_path = None
    backend = None
    access_token_body = None
    user_data_body = None
    user_data_url = ''
    user_data_content_type = 'text/json'
    expected_username = ''
    settings = None
    partial_login_settings = None
    request_token_body = None

    def __init__(self, *args, **kwargs):
        self.backend = module_member(self.backend_path)
        self.complete_url = '/complete/{0}/?{1}&{2}'.format(
            self.backend.name,
            'oauth_verifier=bazqux',
            'oauth_token=foobar'
        )
        super(OAuth1Test, self).__init__(*args, **kwargs)

    def setUp(self):
        HTTPretty.enable()
        self.strategy = TestStrategy(self.backend, TestStorage)
        User.reset_cache()
        TestUserSocialAuth.reset_cache()
        TestNonce.reset_cache()
        TestAssociation.reset_cache()

    def tearDown(self):
        self.strategy = None
        User.reset_cache()
        TestUserSocialAuth.reset_cache()
        TestNonce.reset_cache()
        TestAssociation.reset_cache()
        HTTPretty.disable()

    def do_start(self):
        name = self.backend.name.upper().replace('-', '_')
        self.strategy.set_settings({
            'SOCIAL_AUTH_' + name + '_KEY': 'a-key',
            'SOCIAL_AUTH_' + name + '_SECRET': 'a-secret-key',
        })
        HTTPretty.register_uri(HTTPretty.GET, self.backend.REQUEST_TOKEN_URL,
                               status=200, body=self.request_token_body)

        start_url = self.strategy.start().url
        target_url = self.strategy.build_absolute_uri(self.complete_url)
        target_query = parse_qs(urlparse(target_url).query)

        HTTPretty.register_uri(HTTPretty.GET, start_url, status=301,
                               location=target_url)
        HTTPretty.register_uri(HTTPretty.GET, target_url, status=200,
                               body='foobar')

        response = requests.get(start_url)
        expect(response.url).to.equal(target_url)
        expect(response.text).to.equal('foobar')

        method = self.backend.ACCESS_TOKEN_METHOD == 'GET' and HTTPretty.GET \
                                                            or HTTPretty.POST
        HTTPretty.register_uri(method,
                               uri=self.backend.ACCESS_TOKEN_URL,
                               status=200,
                               body=self.access_token_body or '',
                               content_type='text/json')

        if self.user_data_url:
            HTTPretty.register_uri(HTTPretty.GET, self.user_data_url,
                                   body=self.user_data_body or '',
                                   content_type=self.user_data_content_type)
        self.strategy.set_request_data(target_query)

    def do_login(self):
        self.do_start()
        user = self.strategy.complete()
        expect(user.username).to.equal(self.expected_username)

    def do_partial_pipeline(self):
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
        self.do_start()
        url = self.strategy.build_absolute_uri('/password')
        redirect = self.strategy.complete()
        expect(redirect.url).to.equal(url)

        HTTPretty.register_uri(HTTPretty.GET, redirect.url, status=200,
                               body='foobar')
        HTTPretty.register_uri(HTTPretty.POST, redirect.url, status=200)

        password = 'foobar'
        requests.get(url)
        requests.post(url, data={'password': password})

        data = parse_qs(HTTPretty.last_request.body)
        expect(data['password']).to.equal(password)
        self.strategy.session_set('password', data['password'])

        data = self.strategy.session_pop('partial_pipeline')
        idx, xargs, xkwargs = self.strategy.from_session(data)
        user = self.strategy.continue_pipeline(pipeline_index=idx,
                                               *xargs, **xkwargs)

        expect(user.username).to.equal(self.expected_username)
        expect(user.password).to.equal(password)
