"""
Yammer OAuth2 support
"""
from social.utils import parse_qs
from social.backends.oauth import BaseOAuth2


class YammerOAuth2(BaseOAuth2):
    name = 'yammer'
    AUTHORIZATION_URL = 'https://www.yammer.com/dialog/oauth'
    ACCESS_TOKEN_URL = 'https://www.yammer.com/oauth2/access_token'
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires'),
        ('mugshot_url', 'mugshot_url')
    ]

    def get_user_id(self, details, response):
        return response['user']['id']

    def get_user_details(self, response):
        username = response['user']['name']
        first_name = response['user']['first_name']
        last_name = response['user']['last_name']
        full_name = response['user']['full_name']
        email = response['user']['contact']['email_addresses'][0]['address']
        mugshot_url = response['user']['mugshot_url']
        return {
            'username': username,
            'email': email,
            'fullname': full_name,
            'first_name': first_name,
            'last_name': last_name,
            'picture_url': mugshot_url
        }

    def auth_complete(self, *args, **kwargs):
        """Yammer API is a little strange"""
        self.process_error(self.data)
        # now we need to clean up the data params
        data = self.data.copy()
        redirect_state = data.get('redirect_state')
        if redirect_state and '?' in redirect_state:
            redirect_state, extra = redirect_state.split('?', 1)
            extra = parse_qs(extra)
            data['redirect_state'] = redirect_state
            if 'code' in extra:
                data['code'] = extra['code']
        self.data = data
        return super(YammerOAuth2, self).auth_complete(*args, **kwargs)


class YammerStagingOAuth2(YammerOAuth2):
    name = 'yammer-staging'
    AUTHORIZATION_URL = 'https://www.staging.yammer.com/dialog/oauth'
    ACCESS_TOKEN_URL = 'https://www.staging.yammer.com/oauth2/access_token'
    REQUEST_TOKEN_URL = 'https://www.staging.yammer.com/oauth2/request_token'
