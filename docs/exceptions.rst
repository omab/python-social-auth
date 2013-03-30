Exceptions
==========

This set of exceptions were introduced to describe the situations a bit more
than just the ``ValueError`` usually raised.

``SocialAuthBaseException``
    Base class for all social auth exceptions.

``AuthException``
    Base exception class for authentication process errors.

``AuthFailed``
    Authentication failed for some reason.

``AuthCanceled``
    Authentication was canceled by the user.

``AuthUnknownError``
    An unknown error stoped the authentication process.

``AuthTokenError``
    Unauthorized or access token error, it was invalid, impossible to
    authenticate or user removed permissions to it.

``AuthMissingParameter``
    A needed parameter to continue the process was missing, usually raised by
    the services that need some POST data like myOpenID.

``AuthAlreadyAssociated``
    A different user has already associated the social account that the current
    user is trying to associate.

``WrongBackend``
    Raised when the backend given in the URLs is invalid (not enabled or
    registered).

``NotAllowedToDisconnect``
    Raised on disconnect action when it's not safe for the user to disconnect
    the social account, probably because the user lacks a password or another
    social account.

``AuthStateMissing``
    The state parameter is missing from the server response.

``AuthStateForbidden``
    The state parameter returned by the server is not the one sent.

``AuthTokenRevoked``
    Raised when the user revoked the access_token in the provider.

These are a subclass of ``ValueError`` to keep backward compatibility.
