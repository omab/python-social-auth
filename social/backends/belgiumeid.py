from social.backends.open_id import OpenIdAuth


class BelgiumEIDOpenId(OpenIdAuth):
    """Belgium e-ID OpenID authentication backend"""
    name = 'belgiumeid'
    URL = 'https://www.e-contract.be/eid-idp/endpoints/openid/auth'
