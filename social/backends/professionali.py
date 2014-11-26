# -*- coding: utf-8 -*-
"""
professionaly OAuth 2.0 support.

This contribution adds support for professionaly.ru OAuth 2.0.
Username is retrieved from the identity returned by server.
"""
from time import time

from social.backends.oauth import BaseOAuth2
from social.utils import parse_qs


class ProfessionaliOAuth2(BaseOAuth2):
    name = 'professionali'
    ID_KEY = 'user_id'
    EXTRA_DATA = [('avatar_big', 'avatar_big'),
                  ('link', 'link')]
    AUTHORIZATION_URL = 'https://api.professionali.ru/oauth/authorize.html'
    ACCESS_TOKEN_URL = 'https://api.professionali.ru/oauth/getToken.json'
    ACCESS_TOKEN_METHOD = 'POST'

    def get_user_details(self, response):
        first_name, last_name = map(response.get, ('firstname', 'lastname'))
        email = (self.setting('FAKE_EMAIL')
                 and '%s@professionali.ru' % time()
                 or '')
        return {'username': '%s_%s' % (last_name, first_name),
                'first_name': first_name,
                'last_name': last_name,
                'email': email}

    def user_data(self, access_token, response, *args, **kwargs):
        url = 'https://api.professionali.ru/v6/users/get.json'
        default_fields = list(set(['firstname', 'lastname',
                                   'avatar_big', 'link']
                                  + self.setting('EXTRA_DATA', [])))
        fields = ','.join(default_fields)
        params = {'fields': fields,
                  'access_token': access_token,
                  'ids[]': response['user_id']}
        try:
            return self.get_json(url, params)[0]
        except (TypeError, KeyError, IOError, ValueError, IndexError):
            return None

    def get_json(self, url, *args, **kwargs):
        return self.request(url, verify=False, *args, **kwargs).json()

    def get_querystring(self, url, *args, **kwargs):
        return parse_qs(self.request(url, verify=False, *args, **kwargs).text)
