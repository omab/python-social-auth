DailyMotion
===========

DailyMotion uses OAuth2. In order to enable the backend follow:

- Register an application at `DailyMotion Developer Portal`_

- Fill in the **Client Id** and **Client Secret** values in your settings::

    SOCIAL_AUTH_DAILYMOTION_KEY = ''
    SOCIAL_AUTH_DAILYMOTION_SECRET = ''
    
- Set the ``Callback URL`` to ``http://<your hostname>/complete/dailymotion/``

- Specify scopes with::

    SOCIAL_AUTH_DAILYMOTION_SCOPE = [...]
    
  Available scopes are listed in the `Requesting Extended Permissions`_
  section.

.. _DailyMotion Developer Portal: http://www.dailymotion.com/profile/developer/new
.. _Requesting Extended Permissions: http://www.dailymotion.com/doc/api/authentication.html#requesting-extended-permissions
