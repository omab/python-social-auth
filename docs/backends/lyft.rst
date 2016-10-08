Lyft
=========

Lyft implements OAuth2 as its authorization service. To setup a Lyft backend:

1. Register a new application via the `Lyft Developer Portal`_.

2. Add the Lyft OAuth2 backend as an option in your settings::

      SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
          ...
          'social.backends.lyft.LyftOAuth2',
          ...
      )

3. Use the ``Client Id`` and ``Client Secret`` from the Developer Portal into your settings::

      SOCIAL_AUTH_LYFT_KEY = ''
      SOCIAL_AUTH_LYFT_SECRET = ''

4. Specify the scope that your app should have access to::

    SOCIAL_AUTH_LYFT_SCOPE = ['public', 'profile', 'rides.read', 'rides.request']

To learn more about the API and the calls that are available, read the `Lyft API Documentation`_.

.. _Lyft Developer Portal: https://developer.lyft.com/
.. _Lyft API Documentation: https://developer.lyft.com/docs
