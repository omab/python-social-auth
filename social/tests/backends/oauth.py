import requests

from sure import expect
from httpretty import HTTPretty

from social.p3 import urlparse
from social.utils import parse_qs

from social.tests.models import User
from social.tests.backends.base import BaseBackendTest


class BaseOAuthTest(BaseBackendTest):
    backend = None
    backend_path = None
    user_data_body = None
    user_data_url = ''
    user_data_content_type = 'application/json'
    access_token_body = None
    access_token_status = 200
    expected_username = ''

    def extra_settings(self):
        return {'SOCIAL_AUTH_' + self.name + '_KEY': 'a-key',
                'SOCIAL_AUTH_' + self.name + '_SECRET': 'a-secret-key'}

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
