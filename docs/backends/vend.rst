Vend
====

Vend supports OAuth 2.

- Register a new application at `Vend Developers Portal`_
  
- Add the Vend OAuth2 backend to your settings page::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.vend.VendOAuth2',
        ...
    )

- Fill ``App Key`` and ``App Secret`` values in the settings::

      SOCIAL_AUTH_VEND_OAUTH2_KEY = ''
      SOCIAL_AUTH_VEND_OAUTH2_SECRET = ''

More details on their docs_.

.. _Vend Developers Portal: https://developers.vendhq.com/developer/applications
.. _docs: https://developers.vendhq.com/documentation
