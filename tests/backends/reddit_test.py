import json

from tests.oauth import OAuth2Test


class RedditOAuth2Test(OAuth2Test):
    backend_path = 'social.backends.reddit.RedditOAuth2'
    user_data_url = 'https://oauth.reddit.com/api/v1/me.json'
    expected_username = 'foobar'
    access_token_body = json.dumps({
        'name': 'foobar',
        'created': 1203420772.0,
        'access_token': 'foobar-token',
        'created_utc': 1203420772.0,
        'expires_in': 3600.0,
        'link_karma': 34,
        'token_type': 'bearer',
        'comment_karma': 167,
        'over_18': True,
        'is_gold': False,
        'is_mod': True,
        'scope': 'identity',
        'has_verified_email': False,
        'id': '33bma',
        'refresh_token': 'foobar-refresh-token'
    })
    user_data_body = json.dumps({
        'name': 'foobar',
        'created': 1203420772.0,
        'created_utc': 1203420772.0,
        'link_karma': 34,
        'comment_karma': 167,
        'over_18': True,
        'is_gold': False,
        'is_mod': True,
        'has_verified_email': False,
        'id': '33bma'
    })

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()
