import sys
import json
from urllib import urlencode

sys.path.insert(0, '..')

from social.backends.facebook import FacebookOAuth2
from tests.oauth2_tests import OAuth2Test


class FacebookTest(OAuth2Test):
    backend = FacebookOAuth2
    complete_url = '/complete/facebook/?code=foobar'
    user_data_url = 'https://graph.facebook.com/me'
    access_token_body = urlencode({
        'access_token': 'foobar',
        'token_type': 'bearer'
    })
    user_data_body = json.dumps({
        'username': 'foobar',
        'first_name': 'Foo',
        'last_name': 'Bar',
        'verified': True,
        'name': 'Foo Bar',
        'gender': 'male',
        'updated_time': '2013-02-13T14:59:42+0000',
        'link': 'http://www.facebook.com/foobar',
        'id': '110011001100010'
    })
    settings = {
        'SOCIAL_AUTH_FACEBOOK_KEY': 'a-key',
        'SOCIAL_AUTH_FACEBOOK_SECRET': 'a-secret-key'
    }
    expected_username = 'foobar'

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()
