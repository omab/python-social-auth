Vimeo
=====

Vimeo uses OAuth1 to grant access to their API. In order to get the backend
running follow:

- Register an application at `Vimeo Developer Portal`_ filling the required
  settings. Ensure to fill ``App Callback URL`` field with
  ``http://<your hostname>/complete/vimeo/``

- Fill in the **Client Id** and **Client Secret** values in your settings::

    SOCIAL_AUTH_VIMEO_KEY = ''
    SOCIAL_AUTH_VIMEO_SECRET = ''
    
- Specify scopes with::

    SOCIAL_AUTH_VIMEO_SCOPE = [...]

- Add the backend to ``AUTHENTICATION_BACKENDS``::

    AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.vimeo.VimeoOAuth1',
        ...
    )

.. _Vimeo Developer Portal: https://developer.vimeo.com/apps/new
