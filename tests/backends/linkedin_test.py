import json

from social.p3 import urlencode
from tests.oauth import OAuth1Test, OAuth2Test


class LinkedinOAuth1Test(OAuth1Test):
    backend_path = 'social.backends.linkedin.LinkedinOAuth'
    user_data_url = 'https://api.linkedin.com/v1/people/~:' \
                        '(first-name,id,last-name)'
    expected_username = 'FooBar'
    access_token_body = json.dumps({
        'access_token': 'foobar',
        'token_type': 'bearer'
    })
    request_token_body = urlencode({
        'oauth_token_secret': 'foobar-secret',
        'oauth_token': 'foobar',
        'oauth_callback_confirmed': 'true'
    })
    user_data_body = json.dumps({
        'lastName': 'Bar',
        'id': '1010101010',
        'firstName': 'Foo'
    })

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()


class LinkedinOAuth2Test(OAuth2Test):
    backend_path = 'social.backends.linkedin.LinkedinOAuth2'
    user_data_url = 'https://api.linkedin.com/v1/people/~:' \
                        '(first-name,id,last-name)'
    expected_username = 'FooBar'
    access_token_body = json.dumps({
        'access_token': 'foobar',
        'token_type': 'bearer'
    })
    request_token_body = urlencode({
        'oauth_token_secret': 'foobar-secret',
        'oauth_token': 'foobar',
        'oauth_callback_confirmed': 'true'
    })
    user_data_body = json.dumps({
        'lastName': 'Bar',
        'id': '1010101010',
        'firstName': 'Foo'
    })

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()
