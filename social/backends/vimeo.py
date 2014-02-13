from social.backends.oauth import BaseOAuth1


class VimeoOAuth1(BaseOAuth1):
    """Vimeo OAuth authentication backend"""
    name = 'vimeo'
    AUTHORIZATION_URL = 'https://vimeo.com/oauth/authorize'
    REQUEST_TOKEN_URL = 'https://vimeo.com/oauth/request_token'
    ACCESS_TOKEN_URL = 'https://vimeo.com/oauth/access_token'

    def get_user_id(self, details, response):
        return response.get('person', {}).get('id')

    def get_user_details(self, response):
        """Return user details from Twitter account"""
        person = response.get('person', {})
        fullname = person.get('display_name', '')
        if ' ' in fullname:
            first_name, last_name = fullname.split(' ', 1)
        else:
            first_name, last_name = fullname, ''
        return {'username': person.get('username', ''),
                'email': '',
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        return self.get_json(
            'https://vimeo.com/api/rest/v2',
            params={'format': 'json', 'method': 'vimeo.people.getInfo'},
            auth=self.oauth_auth(access_token)
        )
