Yahoo OAuth
===========

OAuth 1.0 workflow, useful if you are planning to use Yahoo's API.

- Register a new application at `Yahoo Developer Center`_, set your app domain
  and configure scopes (they can't be overriden by application).

- Fill ``Consumer Key`` and ``Consumer Secret`` values in the settings::

      SOCIAL_AUTH_YAHOO_KEY = ''
      SOCIAL_AUTH_YAHOO_SECRET = ''

.. _Yahoo Developer Center: https://developer.apps.yahoo.com/projects/
