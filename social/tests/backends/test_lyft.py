import json

from social.tests.backends.oauth import OAuth2Test


class LyftOAuth2Test(OAuth2Test):
    backend_path = 'social.backends.lyft.LyftOAuth2'
    access_token_body = json.dumps({
        'access_token': 'foobar',
        'refresh_token': 'barfoo',
        'token_type': 'bearer',
        'expires_in': 3600,
        'scope': 'one two three'
    })
    # expected_username = 'acct_foobar'

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()
