import sys
import json

sys.path.insert(0, '..')

from social.backends.angel import AngelOAuth2
from tests.oauth2_tests import OAuth2Test


class AngelTest(OAuth2Test):
    backend = AngelOAuth2
    user_data_url = 'https://api.angel.co/1/me/'
    access_token_body = json.dumps({
        'access_token': 'foobar',
        'token_type': 'bearer'
    })
    user_data_body = json.dumps({
        'facebook_url': 'http://www.facebook.com/foobar',
        'bio': None,
        'name': 'Foo Bar',
        'roles': [],
        'github_url': None,
        'angellist_url': 'https://angel.co/foobar',
        'image': 'https://graph.facebook.com/foobar/picture?type=square',
        'linkedin_url': None,
        'locations': [],
        'twitter_url': None,
        'what_ive_built': None,
        'dribbble_url': None,
        'behance_url': None,
        'blog_url': None,
        'aboutme_url': None,
        'follower_count': 0,
        'online_bio_url': None,
        'id': 101010
    })
    expected_username = 'foobar'

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()
