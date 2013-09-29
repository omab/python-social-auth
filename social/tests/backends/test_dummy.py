import json
import datetime
import time

from sure import expect
from httpretty import HTTPretty

from social.actions import do_disconnect
from social.backends.oauth import BaseOAuth2
from social.exceptions import AuthForbidden

from social.tests.models import User
from social.tests.backends.oauth import OAuth2Test


class DummyOAuth2(BaseOAuth2):
    name = 'dummy'
    AUTHORIZATION_URL = 'http://dummy.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'http://dummy.com/oauth/access_token'
    REVOKE_TOKEN_URL = 'https://dummy.com/oauth/revoke'
    REVOKE_TOKEN_METHOD = 'GET'
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires'),
        ('empty', 'empty', True),
        'url'
    ]

    def get_user_details(self, response):
        """Return user details from Github account"""
        return {'username': response.get('username'),
                'email': response.get('email', ''),
                'first_name': response.get('first_name', ''),
                'last_name': response.get('last_name', '')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json('http://dummy.com/user', params={
            'access_token': access_token
        })


class DummyOAuth2Test(OAuth2Test):
    backend_path = 'social.tests.backends.test_dummy.DummyOAuth2'
    user_data_url = 'http://dummy.com/user'
    expected_username = 'foobar'
    access_token_body = json.dumps({
        'access_token': 'foobar',
        'token_type': 'bearer'
    })
    user_data_body = json.dumps({
        'id': 1,
        'username': 'foobar',
        'url': 'http://dummy.com/user/foobar',
        'first_name': 'Foo',
        'last_name': 'Bar',
        'email': 'foo@bar.com'
    })

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()

    def test_tokens(self):
        user = self.do_login()
        expect(user.social[0].tokens).to.equal('foobar')

    def test_revoke_token(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_REVOKE_TOKENS_ON_DISCONNECT': True
        })
        self.do_login()
        user = User.get(self.expected_username)
        user.password = 'password'
        backend = self.backend
        HTTPretty.register_uri(self._method(backend.REVOKE_TOKEN_METHOD),
                               backend.REVOKE_TOKEN_URL,
                               status=200)
        do_disconnect(self.strategy, user)


class WhitelistEmailsTest(DummyOAuth2Test):
    def test_valid_login(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_WHITELISTED_EMAILS': ['foo@bar.com']
        })
        self.do_login()

    def test_invalid_login(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_WHITELISTED_EMAILS': ['foo2@bar.com']
        })
        self.do_login.when.called_with().should.throw(AuthForbidden)


class WhitelistDomainsTest(DummyOAuth2Test):
    def test_valid_login(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_WHITELISTED_DOMAINS': ['bar.com']
        })
        self.do_login()

    def test_invalid_login(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_WHITELISTED_EMAILS': ['bar2.com']
        })
        self.do_login.when.called_with().should.throw(AuthForbidden)


DELTA = datetime.timedelta(days=1)


class ExpirationTimeTest(DummyOAuth2Test):
    user_data_body = json.dumps({
        'id': 1,
        'username': 'foobar',
        'url': 'http://dummy.com/user/foobar',
        'first_name': 'Foo',
        'last_name': 'Bar',
        'email': 'foo@bar.com',
        'expires': time.mktime((datetime.datetime.utcnow() +
                                DELTA).timetuple())
    })

    def test_expires_time(self):
        user = self.do_login()
        social = user.social[0]
        expiration = social.expiration_datetime()
        expect(expiration <= DELTA).to.equal(True)
