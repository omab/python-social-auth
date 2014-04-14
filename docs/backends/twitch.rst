Twitch
======

Twitch works similar to Facebook (OAuth).

- Register a new application in the `connections tab`_ of your Twitch settings page, set the callback URL to
  ``http://example.com/complete/twitch/`` replacing ``example.com`` with your domain.

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_TWITCH_KEY = ''
      SOCIAL_AUTH_TWITCH_SECRET = ''

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_TWITCH_SCOPE = [...]

.. _connections tab: http://www.twitch.tv/settings/connections
