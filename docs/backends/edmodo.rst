Edmodo
======

Edmodo supports OAuth 2.

- Register a new application at `Edmodo Connect API`_, and follow the
  instructions below.
- Add the Edmodo OAuth2 backend to your settings page::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.edmodo.EdmodoOAuth2',
        ...
    )

- Fill ``App Key``, ``App Secret`` and ``App Scope`` values in the settings::

      SOCIAL_AUTH_EDMODO_OAUTH2_KEY = ''
      SOCIAL_AUTH_EDMODO_OAUTH2_SECRET = ''
      SOCIAL_AUTH_EDMODO_SCOPE = ['basic']

.. _Edmodo Connect API: https://developers.edmodo.com/edmodo-connect/edmodo-connect-overview-getting-started/
