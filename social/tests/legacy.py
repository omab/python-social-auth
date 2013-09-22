import requests

from sure import expect
from httpretty import HTTPretty

from social.utils import module_member, parse_qs
from social.backends.utils import load_backends
from social.tests.base import BaseBackendTest
from social.tests.strategy import TestStrategy
from social.tests.models import TestStorage, User, TestUserSocialAuth, \
                                TestNonce, TestAssociation


class BaseLegacyTest(BaseBackendTest):
    form = ''
    response_body = ''

    def setUp(self):
        HTTPretty.enable()
        self.backend = module_member(self.backend_path)
        name = self.backend.name.upper().replace('-', '_')
        self.strategy = TestStrategy(self.backend, TestStorage)
        self.complete_url = self.strategy.build_absolute_uri(
            '/complete/{0}'.format(name)
        )
        self.strategy.set_settings({
            'SOCIAL_AUTH_{0}_FORM_URL'.format(name): '/login/{0}'.format(name),
            'SOCIAL_AUTH_AUTHENTICATION_BACKENDS': (
                self.backend_path,
                'social.tests.backends.broken_test.BrokenBackendAuth'
            )
        })
        # Force backends loading to trash PSA cache
        load_backends(
            self.strategy.get_setting('SOCIAL_AUTH_AUTHENTICATION_BACKENDS'),
            force_load=True
        )

    def tearDown(self):
        self.strategy = None
        self.backend = None
        self.complete_url = None
        User.reset_cache()
        TestUserSocialAuth.reset_cache()
        TestNonce.reset_cache()
        TestAssociation.reset_cache()
        HTTPretty.disable()

    def do_start(self):
        start_url = self.strategy.build_absolute_uri(self.strategy.start().url)
        HTTPretty.register_uri(
            HTTPretty.GET,
            start_url,
            status=200,
            body=self.form.format(self.complete_url)
        )
        HTTPretty.register_uri(
            HTTPretty.POST,
            self.complete_url,
            status=200,
            body=self.response_body,
            content_type='application/x-www-form-urlencoded'
        )
        response = requests.get(start_url)
        expect(response.text).to.equal(self.form.format(self.complete_url))
        response = requests.post(
            self.complete_url,
            data=parse_qs(self.response_body)
        )
        self.strategy.set_request_data(parse_qs(response.text))
        return self.strategy.complete()
