"""
LiveJournal OpenId backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/livejournal.html
"""
from social.p3 import urlsplit
from social.backends.open_id import OpenIdAuth
from social.exceptions import AuthMissingParameter


class LiveJournalOpenId(OpenIdAuth):
    """LiveJournal OpenID authentication backend"""
    name = 'livejournal'

    def get_user_details(self, response):
        """Generate username from identity url"""
        values = super(LiveJournalOpenId, self).get_user_details(response)
        values['username'] = values.get('username') or \
                             urlsplit(response.identity_url)\
                                .netloc.split('.', 1)[0]
        return values

    def openid_url(self):
        """Returns LiveJournal authentication URL"""
        if not self.data.get('openid_lj_user'):
            raise AuthMissingParameter(self, 'openid_lj_user')
        return 'http://{0}.livejournal.com'.format(self.data['openid_lj_user'])
