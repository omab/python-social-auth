import json

from social.p3 import urlencode
from social.tests.backends.oauth import OAuth1Test


class ZoteroOAuth1Test(OAuth1Test):
    backend_path = 'social.backends.zotero.ZoteroOAuth'
    expected_username = 'FooBar'


    access_token_body = json.dumps({
        'access_token': {u'oauth_token': u'foobar',
                         u'oauth_token_secret': u'rodgsNDK4hLJU1504Atk131G',
                         u'userID': u'123456_abcdef',
                         u'username': u'anyusername'}})

    request_token_body = urlencode({
        'oauth_token_secret': 'foobar-secret',
        'oauth_token': 'foobar',
        'oauth_callback_confirmed': 'true'
    })

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()
