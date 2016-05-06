Pinterest
=========

Pinterest implemented OAuth2 protocol for their authentication mechanism.
To enable ``python-social-auth`` support follow this steps:

1. Go to `Pinterest developers zone`_ and create an application.

2. Fill App Id and Secret in your project settings::

    SOCIAL_AUTH_PINTEREST_KEY = '...'
    SOCIAL_AUTH_PINTEREST_SECRET = '...'
    SOCIAL_AUTH_PINTEREST_SCOPE = [
        'read_public',
        'write_public',
        'read_relationships',
        'write_relationships'
    ]

3. Enable the backend::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.pinterest.PinterestOAuth2',
        ...
    )

.. _Pinterest developers zone: https://developers.pinterest.com/apps/
.. _Pinterest Documentation: https://developers.pinterest.com/docs/
