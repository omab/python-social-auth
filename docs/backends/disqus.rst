Disqus
======

Disqus uses OAuth v2 for Authentication.

- Register a new application at the `Disqus API`_, and

- fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_DISQUS_KEY = ''
      SOCIAL_AUTH_DISQUS_SECRET = ''

- extra scopes can be defined by using::

    SOCIAL_AUTH_DISQUS_AUTH_EXTRA_ARGUMENTS = {'scope': 'likes comments relationships'}

  Check `Disqus Auth API`_ for details.

.. _Disqus Auth API: http://disqus.com/api/docs/auth/
.. _Disqus API: http://disqus.com/api/applications/
