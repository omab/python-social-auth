import json

from social.p3 import urlencode
from social.exceptions import AuthUnknownError

from social.tests.backends.oauth import OAuth2Test


class FacebookOAuth2Test(OAuth2Test):
    backend_path = 'social.backends.facebook.FacebookOAuth2'
    user_data_url = 'https://graph.facebook.com/me'
    expected_username = 'foobar'
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

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()


class FacebookOAuth2WrongUserDataTest(FacebookOAuth2Test):
    user_data_body = 'null'

    def test_login(self):
        self.do_login.when.called_with().should.throw(AuthUnknownError)

    def test_partial_pipeline(self):
        self.do_partial_pipeline.when.called_with().should.throw(
            AuthUnknownError
        )
