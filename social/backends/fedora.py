"""
Fedora OpenId backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/fedora.html
"""
from social.backends.open_id import OpenIdAuth


class FedoraOpenId(OpenIdAuth):
    name = 'fedora'
    URL = 'https://id.fedoraproject.org'
