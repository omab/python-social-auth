Yammer
======

Yammer users OAuth2 for their auth mechanism, this application supports Yammer
OAuth2 in production and staging modes.

Production Mode
---------------

In order to enable the backend, follow:


- Register an application at `Client Applications`_

- Fill **Client Key** and **Client Secret** settings::

    SOCIAL_AUTH_YAMMER_KEY = '...'
    SOCIAL_AUTH_YAMMER_SECRET = '...'


Staging Mode
------------

Staging mode is configured the same as ``Production Mode``, but settings are
prefixed with::

    SOCIAL_AUTH_YAMMER_STAGING_*

.. _Client Applications: https://www.yammer.com/client_applications
