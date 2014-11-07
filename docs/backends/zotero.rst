Zotero
======

Zotero implements OAuth1 as their authentication mechanism for their Web API v3.


1. Go to the `Zotero app registration page`_ to register your application.

2. Fill the **Client ID** and **Client Secret** in your project settings::

    SOCIAL_AUTH_ZOTERO_KEY = '...'
    SOCIAL_AUTH_ZOTERO_SECRET = '...'

3. Enable the backend::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.amazon.Zotero',
        ...
    )

Further documentation at `Zotero Web API v3 page`_.

.. _Zotero app registration page: https://www.zotero.org/oauth/apps
.. _Zotero Web API v3 page: https://www.zotero.org/support/dev/web_api/v3/start
