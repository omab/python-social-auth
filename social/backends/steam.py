"""Steam OpenId support"""
import re
import json
import urllib

from social.backends.open_id import OpenIdAuth
from social_auth.exceptions import AuthFailed


STEAM_ID = re.compile('steamcommunity.com/openid/id/(.*?)$')
USER_INFO = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?'


class SteamOpenId(OpenIdAuth):
    name = 'steam'
    URL = 'http://steamcommunity.com/openid'

    def get_user_id(self, details, response):
        """Return user unique id provided by service"""
        return self._user_id(response)

    def get_user_details(self, response):
        user_id = self._user_id(response)
        url = USER_INFO + urllib.urlencode({
            'key': self.setting('API_KEY'),
            'steamids': user_id
        })
        details = {}
        try:
            player = json.load(self.urlopen(url))
        except (ValueError, IOError):
            pass
        else:
            if len(player['response']['players']) > 0:
                player = player['response']['players'][0]
                details = {'username': player.get('personaname'),
                           'email': '',
                           'fullname': '',
                           'first_name': '',
                           'last_name': '',
                           'player': player}
        return details

    def _user_id(self, response):
        match = STEAM_ID.search(response.identity_url)
        if match is None:
            raise AuthFailed(self, 'Missing Steam Id')
        return match.group(1)
