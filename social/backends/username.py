"""
Legacy Username backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/username.html
"""
from social.backends.legacy import LegacyAuth


class UsernameAuth(LegacyAuth):
    name = 'username'
    ID_KEY = 'username'
    EXTRA_DATA = ['username']
