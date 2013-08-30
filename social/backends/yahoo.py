"""
Yahoo OpenID support

    No extra configurations are needed to make this work.

OAuth 1.0 Yahoo backend

    Options:
    YAHOO_CONSUMER_KEY
    YAHOO_CONSUMER_SECRET

    References:
        * http://developer.yahoo.com/oauth/guide/oauth-auth-flow.html
        * http://developer.yahoo.com/social/rest_api_guide/
        *           introspective-guid-resource.html
        * http://developer.yahoo.com/social/rest_api_guide/
        *           extended-profile-resource.html

    Scopes:
        To make this extension works correctly you have to have at least
        Yahoo Profile scope with Read permission

    Throws:
        AuthUnknownError - if user data retrieval fails (guid or profile)
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
        if 'emails' in response:
            email = response.get('emails')[0]['handle']
        else:
            email = ''
        return {'username': response.get('nickname'),
                'email': email,
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
