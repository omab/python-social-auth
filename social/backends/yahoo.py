"""
Yahoo OpenID support

No extra configurations are needed to make this work.
"""
from social.backends.open_id import OpenIdAuth


class YahooOpenId(OpenIdAuth):
    """Yahoo OpenID authentication backend"""
    name = 'yahoo'

    def openid_url(self):
        """Return Yahoo OpenID service url"""
        return 'http://me.yahoo.com'


BACKENDS = {
    'yahoo': YahooOpenId,
}
