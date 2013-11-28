Fedora
======

Fedora OpenId doesn't require major settings beside being defined on
``AUTHENTICATION_BACKENDS```::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.fedora.FedoraOpenId',
        ...
    )
