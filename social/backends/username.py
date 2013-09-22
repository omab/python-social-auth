from social.backends.legacy import LegacyAuth


class UsernameAuth(LegacyAuth):
    name = 'username'
    ID_KEY = 'username'
