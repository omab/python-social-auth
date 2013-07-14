"""
AOL OpenID support

No extra configurations are needed to make this work.
"""
from social.backends.open_id import OpenIdAuth


class AOLOpenId(OpenIdAuth):
    name = 'aol'
    URL = 'http://openid.aol.com'
