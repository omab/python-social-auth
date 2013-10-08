"""
OpenSUSE OpenID support

OpenID also works straightforward, it doesn't need further configurations.
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
