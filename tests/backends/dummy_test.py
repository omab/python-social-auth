import json

from social.backends.oauth import BaseOAuth2

from tests.oauth import OAuth2Test


class DummyOAuth2(BaseOAuth2):
    name = 'dummy'
    AUTHORIZATION_URL = 'http://dummy.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'http://dummy.com/oauth/access_token'
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
    backend_path = 'tests.backends.dummy_test.DummyOAuth2'
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
