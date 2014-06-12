Last.fm
=======

Last.fm uses a similar authentication process than OAuth2 but it's not. In
order to enable the support for it just:

- Register an application at `Get an API Account`_, set the Last.fm callback to
  something sensible like http://your.site/complete/lastfm

- Fill in the **API Key** and **API Secret** values in your settings::

    SOCIAL_AUTH_LASTFM_KEY = ''
    SOCIAL_AUTH_LASTFM_SECRET = ''

- Enable the backend in ``AUTHENTICATION_BACKENDS`` setting.
    
.. _Get an API Account: http://www.last.fm/api/account/create
