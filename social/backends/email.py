from social.backends.legacy import LegacyAuth


class EmailAuth(LegacyAuth):
    name = 'email'
    ID_KEY = 'email'
    REQUIRES_EMAIL_VALIDATION = True
