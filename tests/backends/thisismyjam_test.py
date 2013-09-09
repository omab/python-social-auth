import json

from social.p3 import urlencode
from tests.oauth import OAuth1Test


class ThisIsMyJameOAuth1Test(OAuth1Test):
    backend_path = 'social.backends.thisismyjam.ThisIsMyJamOAuth1'
    user_data_url = 'http://api.thisismyjam.com/1/verify.json'
    expected_username = 'foobar'
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
        'id': 10101010,
        'name': 'Foo',
    })

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()
