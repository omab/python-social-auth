"""
Open Suse OpenId backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/suse.html
"""
from social.backends.open_id import OpenIdAuth


class OpenSUSEOpenId(OpenIdAuth):
    name = 'opensuse'
    URL = 'https://www.opensuse.org/openid/user/'

    def get_user_id(self, details, response):
        """
        Return user unique id provided by service. For openSUSE
        the nickname is original.
        """
        return details['nickname']
