import json
from social.tests.backends.oauth import OAuth2Test

class NaverOAuth2Test(OAuth2Test):
    backend_path = 'social.backends.naver.NaverOAuth2'
    user_data_url = 'https://openapi.naver.com/v1/nid/getUserProfile.xml'
    expected_username = 'foobar'
    access_token_body = json.dumps({
        'access_token': 'foobar',
        'token_type': 'bearer',
    })

    user_data_content_type = 'text/xml'
    user_data_body = \
    '<data>' \
        '<result>' \
            '<resultcode>00</resultcode>' \
            '<message>success</message>' \
        '</result>' \
        '<response>' \
            '<nickname>naverIDLogin</nickname>' \
            '<name>userName<name>' \
            '<id>123456</id>' \
            '<gender>M</gender>' \
            '<age>40-49</age>' \
            '<birthday>01-01</birthday>' \
            '<profile_image>http://naver.com/image.url.jpg</profile_image>' \
        '</response>' \
    '</data>'

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()