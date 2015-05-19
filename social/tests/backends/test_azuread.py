"""
Copyright (c) 2015 Microsoft Open Technologies, Inc.

All rights reserved. 

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
from social.p3 import urlencode
from social.tests.backends.oauth import OAuth2Test
from httpretty import HTTPretty
from social.tests.models import User

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
                    '9mdG9ubGluZS5jb20vQ2hhbmdlUGFzc3dvcmQuYXNweCJ9.3V50dHXTZOHj9UWtkn2g7BjX5JxNe8skYlK4PdhiLz4',
        'expires_in': 3600,
        'expires_on': 1423650396,
        'not_before': 1423646496
    })

    refresh_token_body = json.dumps({
        'access_token': 'foobar-new-token',
        'token_type': 'bearer',
        'expires_in': 3600,
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

    # TODO:
    # def test_get_access_token(self):
        # self.do_login()
        # HTTPretty.register_uri(self._method(self.backend.REFRESH_TOKEN_METHOD),
                               # self.backend.REFRESH_TOKEN_URL or
                               # self.backend.ACCESS_TOKEN_URL,
                               # status=200,
                               # body=self.refresh_token_body)
        # user = list(User.cache.values())[0]
        # token = self.backend.get_auth_token(user_id=user.id)
        # self.assertEqual(token, 'foobar-new-token')
        