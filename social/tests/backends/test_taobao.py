import json

from social.tests.backends.oauth import OAuth2Test

TAOBAO_OAUTH_HOST = 'oauth.taobao.com'
# TAOBAO_OAUTH_ROOT = 'authorize'
#Always use secure connection
TAOBAO_OAUTH_REQUEST_TOKEN_URL = 'https://%s/request_token' % (TAOBAO_OAUTH_HOST)
TAOBAO_OAUTH_AUTHORIZATION_URL = 'https://%s/authorize' % (TAOBAO_OAUTH_HOST)
TAOBAO_OAUTH_ACCESS_TOKEN_URL = 'https://%s/token' % (TAOBAO_OAUTH_HOST)

TAOBAO_CHECK_AUTH = 'https://eco.taobao.com/router/rest'
TAOBAO_USER_SHOW = 'https://%s/user/get_user_info' % TAOBAO_OAUTH_HOST
class TaobaoOAuth2Test(OAuth2Test):
    backend_path = 'social.backends.taobao.TAOBAOAuth'
    user_data_url = TAOBAO_CHECK_AUTH
    expected_username = 'foobar'
    access_token_body = json.dumps({
        'access_token': 'foobar',
        'token_type': 'bearer'
        })
    user_data_body = json.dumps( {
        "w2_expires_in": 0,
        "taobao_user_id": "1",
        "taobao_user_nick": "foobar",
        "w1_expires_in": 1800,
        "re_expires_in": 0,
        "r2_expires_in": 0,
        "expires_in": 86400,
        "r1_expires_in": 1800
        })

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()
