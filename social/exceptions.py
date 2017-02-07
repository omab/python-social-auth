from social_core.exceptions import AuthAlreadyAssociated
from social_core.exceptions import AuthCanceled as AuthCanceledBase
from social_core.exceptions import AuthException
from social_core.exceptions import AuthFailed as AuthFailedBase
from social_core.exceptions import AuthForbidden
from social_core.exceptions import AuthMissingParameter
from social_core.exceptions import AuthStateForbidden
from social_core.exceptions import AuthStateMissing
from social_core.exceptions import AuthTokenError
from social_core.exceptions import AuthTokenRevoked
from social_core.exceptions import AuthUnknownError
from social_core.exceptions import AuthUnreachableProvider
from social_core.exceptions import InvalidEmail
from social_core.exceptions import MissingBackend
from social_core.exceptions import NotAllowedToDisconnect
from social_core.exceptions import SocialAuthBaseException
from social_core.exceptions import WrongBackend


class AuthFailed(AuthFailedBase):
    """Auth process failed for some reason."""
    def __str__(self):
        msg = super(AuthFailed, self).__str__()
        if msg == 'access_denied':
            return 'Authentication process was cancelled'
        return 'Authentication failed: {0}'.format(msg)


class AuthCanceled(AuthCanceledBase):
    """Auth process was canceled by user."""
    def __init__(self, *args, **kwargs):
        self.response = kwargs.pop('response', None)
        super(AuthCanceled, self).__init__(*args, **kwargs)

    def __str__(self):
        msg = super(AuthCanceled, self).__str__()
        if msg:
            return 'Authentication process cancelled: {0}'.format(msg)
        return 'Authentication process cancelled'
