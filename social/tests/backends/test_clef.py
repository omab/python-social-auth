import json

from social.tests.backends.oauth import OAuth2Test


class ClefOAuth2Test(OAuth2Test):
    backend_path = 'social.backends.clef.ClefOAuth2'
    user_data_url = 'https://clef.io/api/v1/info'
    expected_username = '123456789'
    access_token_body = json.dumps({
        'access_token': 'foobar'
    })
    user_data_body = json.dumps({
        'info': {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com'
        },
        'clef_id': '123456789'
    })

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()
