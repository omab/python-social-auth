"""
Steam OpenId backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/steam.html
"""
from social.backends.open_id import OpenIdAuth
from social.exceptions import AuthFailed


USER_INFO = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?'


class SteamOpenId(OpenIdAuth):
    name = 'steam'
    URL = 'https://steamcommunity.com/openid'

    def get_user_id(self, details, response):
        """Return user unique id provided by service"""
        return self._user_id(response)

    def get_user_details(self, response):
        player = self.get_json(USER_INFO, params={
            'key': self.setting('SOCIAL_AUTH_STEAM_KEY'),
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

    def consumer(self):
        # Steam seems to support stateless mode only, ignore store
        if not hasattr(self, '_consumer'):
            self._consumer = self.create_consumer()
        return self._consumer

    def _user_id(self, response):
        user_id = response.identity_url.rsplit('/', 1)[-1]
        if not user_id.isdigit():
            raise AuthFailed(self, 'Missing Steam Id')
        return user_id
