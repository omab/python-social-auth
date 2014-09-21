MineID
======

MineID works similar to Facebook (OAuth).

- Register a new application at `MineID.org`_, set the callback URL to
  ``http://example.com/complete/mineid/`` replacing ``example.com`` with your
  domain.

- Fill ``Client ID`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_MINEID_KEY = ''
      SOCIAL_AUTH_MINEID_SECRET = ''


Self-hosted MineID
------------------

Since MineID is an Open Source software and can be self-hosted, you can
change settings to point to your instance::

    SOCIAL_AUTH_MINEID_HOST = 'www.your-mineid-instance.com'
    SOCIAL_AUTH_MINEID_SCHEME = 'https'  # or 'http'

.. _MineID.org: https://www.mineid.org/
