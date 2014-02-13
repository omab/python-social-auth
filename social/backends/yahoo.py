"""
Yahoo OpenId and OAuth1 backends, docs at:
    http://psa.matiasaguirre.net/docs/backends/yahoo.html
"""
from social.backends.open_id import OpenIdAuth
from social.backends.oauth import BaseOAuth1


class YahooOpenId(OpenIdAuth):
    """Yahoo OpenID authentication backend"""
    name = 'yahoo'
    URL = 'http://me.yahoo.com'


class YahooOAuth(BaseOAuth1):
    """Yahoo OAuth authentication backend"""
    name = 'yahoo-oauth'
    ID_KEY = 'guid'
    AUTHORIZATION_URL = 'https://api.login.yahoo.com/oauth/v2/request_auth'
    REQUEST_TOKEN_URL = \
        'https://api.login.yahoo.com/oauth/v2/get_request_token'
    ACCESS_TOKEN_URL = 'https://api.login.yahoo.com/oauth/v2/get_token'
    EXTRA_DATA = [
        ('guid', 'id'),
        ('access_token', 'access_token'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from Yahoo Profile"""
        fname = response.get('givenName')
        lname = response.get('familyName')
        emails = [email for email in response.get('emails', [])
                        if email.get('handle')]
        emails.sort(key=lambda e: e.get('primary', False))
        return {'username': response.get('nickname'),
                'email': emails[0]['handle'] if emails else '',
                'fullname': '{0} {1}'.format(fname, lname),
                'first_name': fname,
                'last_name': lname}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'http://social.yahooapis.com/v1/user/{0}/profile?format=json'
        return self.get_json(
            url.format(self._get_guid(access_token)),
            auth=self.oauth_auth(access_token)
        )['profile']

    def _get_guid(self, access_token):
        """
            Beause you have to provide GUID for every API request
            it's also returned during one of OAuth calls
        """
        return self.get_json(
            'http://social.yahooapis.com/v1/me/guid?format=json',
            auth=self.oauth_auth(access_token)
        )['guid']['value']
