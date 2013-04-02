"""Steam OpenId support"""
import re

from social.backends.open_id import OpenIdAuth
from social_auth.exceptions import AuthFailed


STEAM_ID = re.compile('steamcommunity.com/openid/id/(.*?)$')
USER_INFO = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?'


class SteamOpenId(OpenIdAuth):
    name = 'steam'
    URL = 'https://steamcommunity.com/openid'

    def get_user_id(self, details, response):
        """Return user unique id provided by service"""
        return self._user_id(response)

    def get_user_details(self, response):
        player = self.get_json(USER_INFO, params={
            'key': self.setting('API_KEY'),
            'steamids': self._user_id(response)
        })
        if len(player['response']['players']) > 0:
            player = player['response']['players'][0]
            details = {'username': player.get('personaname'),
                       'email': '',
                       'fullname': '',
                       'first_name': '',
                       'last_name': '',
                       'player': player}
        else:
            details = {}
        return details

    def _user_id(self, response):
        return STEAM_ID.search(response.identity_url)
