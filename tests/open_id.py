# -*- coding: utf-8 -*-
import sys
import requests
import unittest
from openid import oidutil
from HTMLParser import HTMLParser

from sure import expect
from httpretty import HTTPretty

sys.path.insert(0, '..')

from social.utils import parse_qs, module_member
from social.backends.utils import user_backends_data, load_backends

from tests.models import TestStorage, User, TestUserSocialAuth, TestNonce, \
                         TestAssociation
from tests.strategy import TestStrategy


# Patch to remove the too-verbose output until a new version is released
oidutil.log = lambda *args, **kwargs: None


class FormHTMLParser(HTMLParser):
    form = {}
    inputs = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'form':
            self.form.update(attrs)
        elif tag == 'input' and 'name' in attrs:
            self.inputs[attrs['name']] = attrs['value']


class OpenIdTest(unittest.TestCase):
    backend_path = None
    backend = None
    access_token_body = None
    user_data_body = None
    user_data_url = ''
    expected_username = ''
    settings = None
    partial_login_settings = None

    def setUp(self):
        HTTPretty.enable()
        self.backend = module_member(self.backend_path)
        self.complete_url = '/complete/{0}/'.format(self.backend.name)
        self.strategy = TestStrategy(self.backend, TestStorage,
                                     redirect_uri=self.complete_url)
        self.strategy.set_settings({
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
        User.reset_cache()
        TestUserSocialAuth.reset_cache()
        TestNonce.reset_cache()
        TestAssociation.reset_cache()
        HTTPretty.disable()

    def get_form_data(self, html):
        parser = FormHTMLParser()
        parser.feed(html)
        return parser.form, parser.inputs

    def openid_url(self):
        return self.strategy.backend.openid_url()

    def post_start(self):
        pass

    def do_start(self):
        HTTPretty.register_uri(HTTPretty.GET,
                               self.openid_url(),
                               status=200,
                               body=self.discovery_body,
                               content_type='application/xrds+xml')
        start = self.strategy.start()
        self.post_start()
        form, inputs = self.get_form_data(start)
        HTTPretty.register_uri(HTTPretty.POST,
                               form.get('action'),
                               status=200,
                               body=self.server_response)
        response = requests.post(form.get('action'), data=inputs)
        self.strategy.set_request_data(parse_qs(response.content))
        HTTPretty.register_uri(HTTPretty.POST,
                               form.get('action'),
                               status=200,
                               body='is_valid:true\n')
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
