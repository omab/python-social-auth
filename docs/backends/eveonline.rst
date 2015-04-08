EVE Online Single Sign-On (SSO)
===============================

The EVE Single Sign-On (SSO) works similar to GitHub (OAuth2).

- Register a new application at `EVE Developers`_, set the callback URL to
  ``http://example.com/complete/eveonline/`` replacing ``example.com`` with your
  domain.

- Fill the ``Client ID`` and ``Secret Key`` values from EVE Developers in the settings::

      SOCIAL_AUTH_EVEONLINE_KEY = ''
      SOCIAL_AUTH_EVEONLINE_SECRET = ''

- If you want to use EVE Character names as user names, use this setting::

      SOCIAL_AUTH_CLEAN_USERNAMES = False

- If you want to access EVE Online's CREST API, use::

      SOCIAL_AUTH_EVEONLINE_SCOPE = ['publicData']

.. _EVE Developers: https://developers.eveonline.com/
