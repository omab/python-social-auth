Behance
=======

Behance uses OAuth2 for its auth mechanism.

- Register a new application at `Behance App Registration`_, set your
  application name, website and redirect URI.

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_BEHANCE_KEY = ''
      SOCIAL_AUTH_BEHANCE_SECRET = ''

- Also it's possible to define extra permissions with::

     SOCIAL_AUTH_BEHANCE_SCOPE = [...]

Check available permissions at `Possible Scopes`_. Also check the rest of their
doc at `Behance Developer Documentation`_.

.. _Behance App Registration: http://www.behance.net/dev/register
.. _Possible Scopes: http://www.behance.net/dev/authentication#scopes
.. _Behance Developer Documentation: http://www.behance.net/dev
