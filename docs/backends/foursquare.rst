Foursquare
==========

Foursquare uses OAuth2. In order to enable the backend follow:

- Register an application at `Foursquare Developers Portal`_,
  set the ``Redirect URI`` to ``http://<your hostname>/complete/foursquare/``

- Fill in the **Client Id** and **Client Secret** values in your settings::

    SOCIAL_AUTH_FOURSQUARE_KEY = ''
    SOCIAL_AUTH_FOURSQUARE_SECRET = ''
    
.. _Foursquare Developers Portal: https://foursquare.com/developers/register
