"""
Kakao OAuth2 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/kakao.html
"""
from social.backends.oauth import BaseOAuth2


class KakaoOAuth2(BaseOAuth2):
    """Kakao OAuth authentication backend"""
    name = 'kakao'
    AUTHORIZATION_URL = 'https://kauth.kakao.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://kauth.kakao.com/oauth/token'
    ACCESS_TOKEN_METHOD = 'POST'

    def get_user_id(self, details, response):
        return response['id']

    def get_user_details(self, response):
        """Return user details from Kakao account"""
        nickname = response['properties']['nickname']
        thumbnail_image = response['properties']['thumbnail_image']
        profile_image = response['properties']['profile_image']
        return {
            'username': nickname,
            'email': '',
            'fullname': '',
            'first_name': '',
            'last_name': ''
        }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json('https://kapi.kakao.com/v1/user/me',
                             params={'access_token': access_token})
