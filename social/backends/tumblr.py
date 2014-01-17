"""
Tumblr OAuth1 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/tumblr.html
"""
from social.utils import first
from social.backends.oauth import BaseOAuth1


class TumblrOAuth(BaseOAuth1):
    name = 'tumblr'
    ID_KEY = 'name'
    AUTHORIZATION_URL = 'http://www.tumblr.com/oauth/authorize'
    REQUEST_TOKEN_URL = 'http://www.tumblr.com/oauth/request_token'
    REQUEST_TOKEN_METHOD = 'POST'
    ACCESS_TOKEN_URL = 'http://www.tumblr.com/oauth/access_token'

    def get_user_id(self, details, response):
        return response['response']['user'][self.ID_KEY]

    def get_user_details(self, response):
        # http://www.tumblr.com/docs/en/api/v2#user-methods
        user_info = response['response']['user']
        data = {'username': user_info['name']}
        blog = first(lambda blog: blog['primary'], user_info['blogs'])
        if blog:
            data['fullname'] = blog['title']
        return data

    def user_data(self, access_token):
        return self.get_json('http://api.tumblr.com/v2/user/info',
                             auth=self.oauth_auth(access_token))
