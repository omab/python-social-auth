"""
Orkut OAuth backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/google.html#orkut
"""
from social.backends.google import GoogleOAuth


class OrkutOAuth(GoogleOAuth):
    """Orkut OAuth authentication backend"""
    name = 'orkut'
    DEFAULT_SCOPE = ['http://orkut.gmodules.com/social/']

    def get_user_details(self, response):
        """Return user details from Orkut account"""
        try:
            emails = response['emails'][0]['value']
        except (KeyError, IndexError):
            emails = ''
        return {'username': response['displayName'],
                'email': emails,
                'fullname': response['displayName'],
                'first_name': response['name']['givenName'],
                'last_name': response['name']['familyName']}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from Orkut service"""
        fields = ','.join(set(['name', 'displayName', 'emails'] +
                          self.setting('EXTRA_DATA', [])))
        scope = self.DEFAULT_SCOPE + self.setting('SCOPE', [])
        params = {'method': 'people.get',
                  'id': 'myself',
                  'userId': '@me',
                  'groupId': '@self',
                  'fields': fields,
                  'scope': self.SCOPE_SEPARATOR.join(scope)}
        url = 'http://www.orkut.com/social/rpc'
        request = self.oauth_request(access_token, url, params)
        return self.get_json(request.to_url())['data']

    def oauth_request(self, token, url, params=None):
        params = params or {}
        scope = self.DEFAULT_SCOPE + self.setting('SCOPE', [])
        params['scope'] = self.SCOPE_SEPARATOR.join(scope)
        return super(OrkutOAuth, self).oauth_request(token, url, params)
