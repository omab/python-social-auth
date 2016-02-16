Itembase
=========

Itembase uses OAuth2 for authentication.

- Register a new application for the `Itembase API`_, and

- Add itembase live backend and/or sandbox backend to ``AUTHENTICATION_BACKENDS``::

      AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.itembase.ItembaseOAuth2',
        'social.backends.itembase.ItembaseOAuth2Sandbox',
        ...
      )

- fill ``Client Id`` and ``Client Secret`` values in the settings::

    SOCIAL_AUTH_ITEMBASE_KEY = ''
    SOCIAL_AUTH_ITEMBASE_SECRET = ''

    SOCIAL_AUTH_ITEMBASE_SANDBOX_KEY = ''
    SOCIAL_AUTH_ITEMBASE_SANDBOX_SECRET = ''


- extra scopes can be defined by using::

    SOCIAL_AUTH_ITEMBASE_SCOPE = ['connection.transaction',
                                  'connection.product',
                                  'connection.profile',
                                  'connection.buyer']
    SOCIAL_AUTH_ITEMBASE_SANDBOX_SCOPE = SOCIAL_AUTH_ITEMBASE_SCOPE

.. _Itembase API: http://developers.itembase.com/authentication/index
