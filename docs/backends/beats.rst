Beats
=======

Beats supports OAuth 2.

- Register a new application at `Beats Music API`_, and follow the
  instructions below.
  
OAuth2
------

Add the Beats OAuth2 backend to your settings page::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.beats.BeatsOAuth2',
        ...
    )

- Fill ``App Key`` and ``App Secret`` values in the settings::

      SOCIAL_AUTH_BEATS_OAUTH2_KEY = ''
      SOCIAL_AUTH_BEATS_OAUTH2_SECRET = ''

.. _Beats Music API: https://developer.beatsmusic.com/docs
