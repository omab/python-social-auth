"""
Fedora OpenID support

No extra configurations are needed to make this work.
"""
from social.backends.open_id import OpenIdAuth


class FedoraOpenId(OpenIdAuth):
    name = 'fedora'
    URL = 'https://id.fedoraproject.org'
