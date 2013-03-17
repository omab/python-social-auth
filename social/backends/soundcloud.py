"""
SoundCloud OAuth2 support.

This contribution adds support for SoundCloud OAuth2 service.

The settings SOUNDCLOUD_CLIENT_ID & SOUNDCLOUD_CLIENT_SECRET must be defined
with the values given by SoundCloud application registration process.

http://developers.soundcloud.com/
http://developers.soundcloud.com/docs

By default account id and token expiration time are stored in extra_data
field, check OAuthBackend class for details on how to extend it.
"""
from social.p3 import urlencode
from social.backends.oauth import BaseOAuth2


class SoundcloudOAuth2(BaseOAuth2):
    """Soundcloud OAuth authentication backend"""
    name = 'soundcloud'
    AUTHORIZATION_URL = 'https://soundcloud.com/connect'
    ACCESS_TOKEN_URL = 'https://api.soundcloud.com/oauth2/token'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('id', 'id'),
        ('refresh_token', 'refresh_token'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from Soundcloud account"""
        fullname = response.get('full_name')
        full_name = fullname.split(' ')
        first_name = full_name[0]
        if len(full_name) > 1:
            last_name = full_name[-1]
        else:
            last_name = ''
        return {'username': response.get('username'),
                'email': response.get('email') or '',
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        try:
            return self.get_json('https://api.soundcloud.com/me.json',
                                 params={'oauth_token': access_token})
        except ValueError:
            return None

    def auth_url(self):
        """Return redirect url"""
        if self.STATE_PARAMETER or self.REDIRECT_STATE:
            # Store state in session for further request validation. The state
            # value is passed as state parameter (as specified in OAuth2 spec),
            # but also added to redirect_uri, that way we can still verify the
            # request if the provider doesn't implement the state parameter.
            # Reuse token if any.
            name = self.name + '_state'
            state = self.strategy.session_get(name) or self.state_token()
            self.strategy.session_set(name, state)
        else:
            state = None

        params = self.auth_params(state)
        params.update(self.get_scope_argument())
        params.update(self.auth_extra_arguments())
        return self.AUTHORIZATION_URL + '?' + urlencode(params)
