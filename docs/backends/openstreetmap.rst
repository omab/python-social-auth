OpenStreetMap
=============

OpenStreetMap supports OAuth 1.0 and 1.0a but 1.0a should be used for the new
applications, as 1.0 is for support of legacy clients only.

Access tokens currently do not expire automatically.

More documentation at `OpenStreetMap Wiki`_:

- Login to your account

- Register your application as OAuth consumer on your `OpenStreetMap user settings page`_, and

- Set ``App Key`` and ``App Secret`` values in the settings::

      SOCIAL_AUTH_OPENSTREETMAP_KEY = ''
      SOCIAL_AUTH_OPENSTREETMAP_SECRET = ''

.. _OpenStreetMap Wiki: http://wiki.openstreetmap.org/wiki/OAuth
.. _OpenStreetMap user settings page: http://www.openstreetmap.org/user/username/oauth_clients/new
