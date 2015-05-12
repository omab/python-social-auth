import json
from social.p3 import urlencode
from social.tests.backends.oauth import OAuth2Test

class AzureADOAuth2Test(OAuth2Test):

    backend_path = 'social.backends.azuread.AzureADOAuth2'
    user_data_url = 'https://graph.windows.net/me'
    expected_username = 'foobar'

    access_token_body = json.dumps({
        'access_token': 'foobar',
        'token_type': 'bearer',
        'id_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC83Mjc0MDZhYy03MDY4'
                    'LTQ4ZmEtOTJiOS1jMmQ2NzIxMWJjNTAvIiwiaWF0IjpudWxsLCJleHAiOm51bGwsImF1ZCI6IjAyOWNjMDEwLWJiNzQtNGQyY'
                    'i1hMDQwLWY5Y2VkM2ZkMmM3NiIsInN1YiI6InFVOHhrczltSHFuVjZRMzR6aDdTQVpvY2loOUV6cnJJOW1wVlhPSWJWQTgiLC'
                    'J2ZXIiOiIxLjAiLCJ0aWQiOiI3Mjc0MDZhYy03MDY4LTQ4ZmEtOTJiOS1jMmQ2NzIxMWJjNTAiLCJvaWQiOiI3ZjhlMTk2OS0'
                    '4YjgxLTQzOGMtOGQ0ZS1hZDZmNTYyYjI4YmIiLCJ1cG4iOiJmb29iYXJAdGVzdC5vbm1pY3Jvc29mdC5jb20iLCJnaXZlbl9u'
                    'YW1lIjoiZm9vIiwiZmFtaWx5X25hbWUiOiJiYXIiLCJuYW1lIjoiZm9vIGJhciIsInVuaXF1ZV9uYW1lIjoiZm9vYmFyQHRlc'
                    '3Qub25taWNyb3NvZnQuY29tIiwicHdkX2V4cCI6IjQ3MzMwOTY4IiwicHdkX3VybCI6Imh0dHBzOi8vcG9ydGFsLm1pY3Jvc2'
                    '9mdG9ubGluZS5jb20vQ2hhbmdlUGFzc3dvcmQuYXNweCJ9.3V50dHXTZOHj9UWtkn2g7BjX5JxNe8skYlK4PdhiLz4'
    })

    refresh_token_body = json.dumps({
        'access_token': 'foobar-new-token',
        'token_type': 'bearer',
        'expires_in': 3600.0,
        'refresh_token': 'foobar-new-refresh-token',
        'scope': 'identity'
    })

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()

    def test_refresh_token(self):
        user, social = self.do_refresh_token()
        self.assertEqual(social.extra_data['access_token'], 'foobar-new-token')