MSN Live Connect
================

Live uses OAuth2 for its connect workflow, notice that it isn't OAuth WRAP.

- Register a new application at `Live Connect Developer Center`_, set your site
  domain as redirect domain,

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_LIVE_KEY = ''
      SOCIAL_AUTH_LIVE_SECRET = ''

- Also it's possible to define extra permissions with::

     SOCIAL_AUTH_LIVE_SCOPE = [...]

  Defaults are ``wl.basic`` and ``wl.emails``. Latter one is necessary to
  retrieve user email.

.. _Live Connect Developer Center: https://account.live.com/developers/applications/create
