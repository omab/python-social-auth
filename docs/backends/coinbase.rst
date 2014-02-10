Coinbase
========

Coinbase uses OAuth2.

- Register an application at Coinbase_

- Fill in the **Client Id** and **Client Secret** values in your settings::

    SOCIAL_AUTH_COINBASE_KEY = ''
    SOCIAL_AUTH_COINBASE_SECRET = ''
    
- Set the ``redirect_url`` on coinbase. Make sure to include the trailing
  slash, eg. ``http://hostname/complete/coinbase/``

- Specify scopes with::

    SOCIAL_AUTH_COINBASE_SCOPE = [...]
    
  By default the scope is set to ``balance``.

.. _Coinbase: https://coinbase.com/oauth/applications
