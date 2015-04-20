ChangeTip
=====

ChangeTip

- Register a new application at ChangeTip_, set the callback URL to
  ``http://example.com/complete/changetip/`` replacing ``example.com`` with your
  domain.

- Fill ``Client ID`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_CHANGETIP_KEY = ''
      SOCIAL_AUTH_CHANGETIP_SECRET = ''

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_CHANGETIP_SCOPE = [...]

  See auth scopes at `ChangeTip OAuth docs`_.


.. _ChangeTip: https://www.changetip.com/api
