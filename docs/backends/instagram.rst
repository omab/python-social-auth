Instagram
=========

Instagram uses OAuth v2 for Authentication.

- Register a new application at the `Instagram API`_, and

- fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_INSTAGRAM_KEY = ''
      SOCIAL_AUTH_INSTAGRAM_SECRET = ''

- extra scopes can be defined by using::

    SOCIAL_AUTH_INSTAGRAM_AUTH_EXTRA_ARGUMENTS = {'scope': 'likes comments relationships'}

.. _Instagram API: http://instagr.am/developer/
