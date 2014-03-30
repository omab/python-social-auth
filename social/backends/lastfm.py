from social.backends.base import BaseAuth
from social.backends.oauth import BaseOAuth1
from social.exceptions import AuthException
import hashlib
import json
import logging
import urllib

class LastFmAuth(BaseAuth):
    """Last.Fm authentication backend. Requires two settings: LASTFM_API_KEY and LASTFM_SECRET.
    Don't forget to set the Last.fm callback to something sensible (http://your.site/lastfm/complete)."""
    # Similar to OAuth.
    # 1. Server redirects user to http://www.last.fm/api/auth with the api key (LASTFM_API_KEY).
    # 2. Last.fm asks user to authorize. If user agrees, user is redirected to a callback url (/lastfm/complete) with a temporary token.
    # 3. Server builds a signed request using the temporary token and sends it to Last.fm.
    # 4. Last.fm responds with a username and session key.
    # 5. User is logged in.
    #    The session key can be used by the server to make signed requests on behalf of the user.

    name = "lastfm"
    EXTRA_DATA = [
        ('key', 'session_key')
    ]

    def auth_url(self):
        return "http://www.last.fm/api/auth/?api_key={api_key}".format(api_key=self.setting('LASTFM_API_KEY'))

    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""

        # Sign session request.
        signature_base = "api_key{api_key}methodauth.getSessiontoken{token}{secret}".format(
            api_key=self.setting('LASTFM_API_KEY'),
            token=self.data['token'],
            #secret=settings.LASTFM_SECRET,
            secret=self.setting('LASTFM_SECRET'),
        )
        signature = hashlib.md5(signature_base).hexdigest()
        logging.debug("Generated signature {signature} from {signature_base}".format(signature=signature, signature_base=signature_base))

        session_key_request_template = "http://ws.audioscrobbler.com/2.0/?method=auth.getSession&api_key={api_key}&token={token}&api_sig={api_sig}&format=json"
        session_key_request = session_key_request_template.format(
            api_key=self.setting('LASTFM_API_KEY'),
            token=self.data['token'],
            api_sig=signature,
        )
        urlopener = urllib.FancyURLopener()
        logging.debug("Requesting session key for token {token} using signature {signature}".format(token=self.data['token'], signature=signature))
        # {"session":{"name":"xxxxxxxx","key":"xxxxxxxxx","subscriber":"0"}}
        session_request_response = urlopener.open(session_key_request, signature).read()
        logging.debug("Last.fm responded with {response} for session key request {request}".format(
            response=session_request_response,
            request=session_key_request,
        ))

        kwargs.update({'response': json.loads(session_request_response)['session'], 'backend': self})
        return self.strategy.authenticate(*args, **kwargs)

    def get_user_id(self, details, response):
        """Return a unique ID for the current user, by default from server
        response."""
        return response.get('name')

    def get_user_details(self, response):
        """
        """
        return {
            'username': response['name'],
            'email': '',
            'fullname': response['name'],
            'first_name': '',
            'last_name': '',
        }

