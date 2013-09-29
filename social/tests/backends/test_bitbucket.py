import json
from httpretty import HTTPretty

from social.p3 import urlencode
from social.tests.backends.oauth import OAuth1Test


class BitbucketOAuth1Test(OAuth1Test):
    backend_path = 'social.backends.bitbucket.BitbucketOAuth'
    user_data_url = 'https://bitbucket.org/api/1.0/users/foo@bar.com'
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
    emails_body = json.dumps([{
        'active': True,
        'email': 'foo@bar.com',
        'primary': True
    }])
    user_data_body = json.dumps({
        'user': {
            'username': 'foobar',
            'first_name': 'Foo',
            'last_name': 'Bar',
            'display_name': 'Foo Bar',
            'is_team': False,
            'avatar': 'https://secure.gravatar.com/avatar/'
                      '5280f15cedf540b544eecc30fcf3027c?'
                      'd=https%3A%2F%2Fd3oaxc4q5k2d6q.cloudfront.net%2Fm%2F'
                      '9e262ba34f96%2Fimg%2Fdefault_avatar%2F32%2F'
                      'user_blue.png&s=32',
            'resource_uri': '/1.0/users/foobar'
        }
    })

    def test_login(self):
        HTTPretty.register_uri(HTTPretty.GET,
                               'https://bitbucket.org/api/1.0/emails/',
                               status=200, body=self.emails_body)
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()
