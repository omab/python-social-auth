import json

from social.tests.backends.oauth import OAuth2Test


class DailymotionOAuth2Test(OAuth2Test):
    backend_path = 'social.backends.dailymotion.DailymotionOAuth2'
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
