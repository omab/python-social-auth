import sys
import json

sys.path.insert(0, '..')

from social.backends.dailymotion import DailymotionOAuth2
from tests.oauth2_tests import OAuth2Test


class DailymotionTest(OAuth2Test):
    backend = DailymotionOAuth2
    user_data_url = 'https://api.dailymotion.com/me/'
    expected_username = 'foobar'
    access_token_body = json.dumps({
        'access_token': 'foobar',
        'token_type': 'bearer'
    })
    user_data_body = json.dumps({
        'id': 'foobar',
        'screenname': 'foobar'
    })

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()
