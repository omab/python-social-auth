Uber
=========

Uber uses OAuth v2 for Authentication.

- Register a new application at the `Uber API`_, and follow the instructions below

OAuth2
=========

1. Add the Uber OAuth2 backend to your settings page::

      SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
          ...
          'social.backends.uber.UberOAuth2',
          ...
      )

2. Fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_UBER_KEY = ''
      SOCIAL_AUTH_UBER_SECRET = ''

3. Scope should be defined by using::

    SOCIAL_AUTH_UBER_SCOPE = ['profile', 'request']

.. _Uber API: https://developer.uber.com/dashboard
