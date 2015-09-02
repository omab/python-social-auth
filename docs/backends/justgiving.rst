Just Giving
===========

OAuth2
------

Add the Just Giving OAuth2 backend to your settings page::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.justgiving.JustGivingOAuth2',
        ...
    )

- Fill ``App Key`` and ``App Secret`` values in the settings::

      SOCIAL_AUTH_JUSTGIVING_KEY = ''
      SOCIAL_AUTH_JUSTGIVING_SECRET = ''

.. _Just Giving API Docs: https://api.justgiving.com/docs
