Jawbone
=======

Jawbone uses OAuth2. In order to enable the backend follow:

- Register an application at `Jawbone Developer Portal`_, set the ``OAuth
  redirect URIs`` to ``http://<your hostname>/complete/jawbone/``

- Fill in the **Client Id** and **Client Secret** values in your settings::

    SOCIAL_AUTH_JAWBONE_KEY = ''
    SOCIAL_AUTH_JAWBONE_SECRET = ''
    
- Specify scopes with::

    SOCIAL_AUTH_JAWBONE_SCOPE = [...]
    
  Available scopes are listed in the `Jawbone Authentication Reference`_,
  "socpes" section.

.. _Jawbone Developer Portal: https://jawbone.com/up/developer/account/
.. _Jawbone Authentication Reference: https://jawbone.com/up/developer/authentication
