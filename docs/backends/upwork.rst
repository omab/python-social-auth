Upwork
=======

Upwork supports only OAuth 1.

- Register a new application at `Upwork Developers`_.

OAuth1
------

Add the Upwork OAuth backend to your settings page::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.upwork.UpworkOAuth',
        ...
    )

- Fill ``App Key`` and ``App Secret`` values in the settings::

      SOCIAL_AUTH_UPWORK_KEY = ''
      SOCIAL_AUTH_UPWORK_SECRET = ''

------
For more information please go to `Upwork API Reference`_.

.. Upwork Developers: https://www.upwork.com/services/api/apply
.. Upwork API Reference: https://developers.upwork.com/?lang=python
