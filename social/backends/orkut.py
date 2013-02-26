"""
Orkut OAuth support.

This contribution adds support for Orkut OAuth service. The scope is
limited to http://orkut.gmodules.com/social/ by default, but can be
extended with ORKUT_EXTRA_SCOPE on project settings. Also name, display
name and emails are the default requested user data, but extra values
can be specified by defining ORKUT_EXTRA_DATA setting.

OAuth settings ORKUT_CONSUMER_KEY and ORKUT_CONSUMER_SECRET are needed
to enable this service support.
"""
import json

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
        scope = self.DEFAULT_SCOPE + self.setting('EXTRA_SCOPE', [])
        params = {'method': 'people.get',
                  'id': 'myself',
                  'userId': '@me',
                  'groupId': '@self',
                  'fields': fields,
                  'scope': self.SCOPE_SEPARATOR.join(scope)}
        url = 'http://www.orkut.com/social/rpc'
        request = self.oauth_request(access_token, url, params)
        response = self.urlopen(request.to_url()).read()
        try:
            return json.loads(response)['data']
        except (ValueError, KeyError):
            return None

    def oauth_request(self, token, url, extra_params=None):
        extra_params = extra_params or {}
        scope = self.DEFAULT_SCOPE + self.setting('EXTRA_SCOPE', [])
        extra_params['scope'] = self.SCOPE_SEPARATOR.join(scope)
        return super(OrkutOAuth, self).oauth_request(token, url, extra_params)
