import sys
import requests
import urlparse
import unittest

from sure import expect
from httpretty import HTTPretty

sys.path.insert(0, '..')

from social.utils import parse_qs

from tests.models import TestStorage, User, TestUserSocialAuth, TestNonce, \
                         TestAssociation
from tests.strategy import TestStrategy


class OAuth2Test(unittest.TestCase):
    backend = None
    access_token_body = None
    user_data_body = None
    user_data_url = ''
    expected_username = ''
    settings = None
    partial_login_settings = None

    def __init__(self, *args, **kwargs):
        self.complete_url = '/complete/{0}/?code=foobar'.format(
            self.backend.name
        )
        super(OAuth2Test, self).__init__(*args, **kwargs)

    def setUp(self):
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

    def do_login(self):
        HTTPretty.enable()
        name = self.backend.name.upper().replace('-', '_')
        self.strategy.set_settings({
            'SOCIAL_AUTH_' + name + '_KEY': 'a-key',
            'SOCIAL_AUTH_' + name + '_SECRET': 'a-secret-key',
        })
        start_url = self.strategy.start().url
        target_url = self.strategy.build_absolute_uri(self.complete_url)
        start_query = parse_qs(urlparse.urlparse(start_url).query)

        if self.backend.STATE_PARAMETER:
            location_url = target_url + ('?' in target_url and '&' or '?') + \
                           'state=' + start_query['state']
        elif self.backend.REDIRECT_STATE:
            location_url = target_url + ('?' in target_url and '&' or '?') + \
                           'redirect_state=' + start_query['redirect_state']
        else:
            location_url = target_url
        location_query = parse_qs(urlparse.urlparse(location_url).query)

        HTTPretty.register_uri(HTTPretty.GET, start_url, status=301,
                               location=location_url)
        HTTPretty.register_uri(HTTPretty.GET, location_url, status=200,
                               body='foobar')

        response = requests.get(start_url)
        expect(response.url).to.equal(location_url)
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
                                   content_type='text/json')

        self.strategy.set_request_data(location_query)
        user = self.strategy.complete()
        expect(user.username).to.equal(self.expected_username)
        HTTPretty.disable()

    def do_partial_pipeline(self):
        HTTPretty.enable()
        name = self.backend.name.upper().replace('-', '_')
        self.strategy.set_settings({
            'SOCIAL_AUTH_' + name + '_KEY': 'a-key',
            'SOCIAL_AUTH_' + name + '_SECRET': 'a-secret-key',
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
        start_url = self.strategy.start().url
        target_url = self.strategy.build_absolute_uri(self.complete_url)
        start_query = parse_qs(urlparse.urlparse(start_url).query)

        if self.backend.STATE_PARAMETER:
            location_url = target_url + ('?' in target_url and '&' or '?') + \
                           'state=' + start_query['state']
        elif self.backend.REDIRECT_STATE:
            location_url = target_url + ('?' in target_url and '&' or '?') + \
                           'redirect_state=' + start_query['redirect_state']
        else:
            location_url = target_url
        location_query = parse_qs(urlparse.urlparse(location_url).query)

        HTTPretty.register_uri(HTTPretty.GET, start_url, status=301,
                               location=location_url)
        HTTPretty.register_uri(HTTPretty.GET, target_url, status=200,
                               body='foobar')

        response = requests.get(start_url)
        expect(response.url).to.equal(location_url)
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
                                   content_type='text/json')

        url = self.strategy.build_absolute_uri('/password')
        self.strategy.set_request_data(location_query)
        redirect = self.strategy.complete()
        expect(redirect.url).to.equal(url)

        HTTPretty.register_uri(HTTPretty.GET, redirect.url, status=200,
                               body='foobar')
        HTTPretty.register_uri(HTTPretty.POST, redirect.url, status=200)

        password = 'foobar'
        response = requests.get(url)
        response = requests.post(url, data={'password': password})

        data = parse_qs(HTTPretty.last_request.body)
        expect(data['password']).to.equal(password)
        self.strategy.session_set('password', data['password'])

        data = self.strategy.session_pop('partial_pipeline')
        idx, xargs, xkwargs = self.strategy.from_session(data)
        user = self.strategy.continue_pipeline(pipeline_index=idx,
                                               *xargs, **xkwargs)

        expect(user.username).to.equal(self.expected_username)
        expect(user.password).to.equal(password)
        HTTPretty.disable()
