from social.backends.oauth import BaseOAuth1


class WithingsOAuth(BaseOAuth1):
    name = 'withings'
    AUTHORIZATION_URL = 'https://oauth.withings.com/account/authorize'
    REQUEST_TOKEN_URL = 'https://oauth.withings.com/account/request_token'
    ACCESS_TOKEN_URL = 'https://oauth.withings.com/account/access_token'
    ID_KEY = 'userid'

    def get_user_details(self, response):
        """Return user details from Withings account"""
        return {'userid': response['access_token']['userid'],
                'email': ''}
