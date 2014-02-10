Stackoverflow
=============

Stackoverflow uses OAuth 2.0

- "Register For An App Key" at the `Stack Exchange API`_ site. Set your OAuth
  domain and application website settings.

- Add the ``Client Id``, ``Client Secret`` and ``API Key`` values in settings::

    SOCIAL_AUTH_STACKOVERFLOW_KEY = ''
    SOCIAL_AUTH_STACKOVERFLOW_SECRET = ''
    SOCIAL_AUTH_STACKOVERFLOW_API_KEY = ''

- You can ask for extra permissions with::

    SOCIAL_AUTH_STACKOVERFLOW_SCOPE = [...]

.. _Stack Exchange API: https://api.stackexchange.com/
