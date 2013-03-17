import json

from tests.oauth2 import OAuth2Test


class GoogleTest(OAuth2Test):
    backend_path = 'social.backends.google.GoogleOAuth2'
    user_data_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    expected_username = 'foo'
    access_token_body = json.dumps({
        'access_token': 'foobar',
        'token_type': 'bearer'
    })
    user_data_body = json.dumps({
        'family_name': 'Bar',
        'name': 'Foo Bar',
        'picture': 'https://lh5.googleusercontent.com/-ui-GqpNh5Ms/'
                   'AAAAAAAAAAI/AAAAAAAAAZw/a7puhHMO_fg/photo.jpg',
        'locale': 'en',
        'gender': 'male',
        'email': 'foo@bar.com',
        'birthday': '0000-01-22',
        'link': 'https://plus.google.com/101010101010101010101',
        'given_name': 'Foo',
        'id': '101010101010101010101',
        'verified_email': True
    })

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()
