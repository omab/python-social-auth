NationBuilder
=============

`NaszaKlasa supports OAuth2`_ as their authentication mechanism. Follow these
steps in order to use it:

- Register a new application at your `NK Developers`_ (define the `Callback
  URL` to ``http://example.com/complete/nk/`` where ``example.com``
  is your domain).

- Fill the ``Client ID`` and ``Client Secret`` values from the newly created
  application::

    SOCIAL_AUTH_NK_KEY = ''
    SOCIAL_AUTH_NK_SECRET = ''

- Enable the backend in ``AUTHENTICATION_BACKENDS`` setting::

    AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.nk.NKOAuth2',
        ...
    )

.. _NaszaKlasa supports OAuth2: https://developers.nk.pl
.. _NK Developers: https://developers.nk.pl/developers/oauth2client/form