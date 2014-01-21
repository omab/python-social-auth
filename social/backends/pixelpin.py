from social.backends.oauth import BaseOAuth2


class PixelPinOAuth2(BaseOAuth2):
    """PixelPin OAuth authentication backend"""
    name = 'pixelpin-oauth2'
    ID_KEY = 'id'
    AUTHORIZATION_URL = 'https://login.pixelpin.co.uk/OAuth2/Flogin.aspx'
    ACCESS_TOKEN_URL = 'https://ws3.pixelpin.co.uk/index.php/api/token'
    ACCESS_TOKEN_METHOD = 'POST'
    REQUIRES_EMAIL_VALIDATION = False
    EXTRA_DATA = [
        ('id', 'id'),
    ]

    def get_user_details(self, response):
        """Return user details from PixelPin account"""
        return {'username': response.get('firstName'),
                'email': response.get('email') or '',
                'first_name': response.get('firstName')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json(
            'https://ws3.pixelpin.co.uk/index.php/api/userdata',
            params={'access_token': access_token}
        )
