
from xml.dom import minidom

from social.backends.oauth import BaseOAuth2

class NaverOAuth2(BaseOAuth2):
    """Naver OAuth authentication backend"""
    name = 'naver'
    AUTHORIZATION_URL = 'https://nid.naver.com/oauth2.0/authorize'
    ACCESS_TOKEN_URL = 'https://nid.naver.com/oauth2.0/token'
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('id', 'id'),
    ]

    def get_user_id(self, details, response):
        return response.get('id')

    def get_user_details(self, response):
        """Return user details from Naver account"""
        return {
            'username': response.get('username'),
            'email': response.get('email'),
            'fullname': response.get('username'),
        }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        dom = minidom.parseString(self.request(
            'https://openapi.naver.com/v1/nid/getUserProfile.xml', 
            method='POST',
            headers={'Authorization': 'Bearer {0}'.format(access_token)}
            ).text.encode('utf-8').strip())

        return {
            'id': dom.getElementsByTagName('id')[0].childNodes[0].data,
            'email': dom.getElementsByTagName('email')[0].childNodes[0].data,
            'username': dom.getElementsByTagName('name')[0].childNodes[0].data,
            'nickname': dom.getElementsByTagName('nickname')[0].childNodes[0].data,
            'gender': dom.getElementsByTagName('gender')[0].childNodes[0].data,
            'age': dom.getElementsByTagName('age')[0].childNodes[0].data,
            'birthday': dom.getElementsByTagName('birthday')[0].childNodes[0].data,
            'profile_image': dom.getElementsByTagName('profile_image')[0].childNodes[0].data,
        }

    def auth_headers(self):
        client_id, client_secret = self.get_key_and_secret()
        return {
            'grant_type': 'authorization_code',
            'code': self.data.get('code'),
            'client_id': client_id,
            'client_secret': client_secret,
        }
