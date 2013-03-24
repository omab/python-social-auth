Rdio
====

Rdio provides OAuth 1 and 2 support for their authentication process.

OAuth 1.0a
----------

To setup Rdio OAuth 1.0a, add the following to your settings page::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.rdio.RdioOAuth1',
        ...
    )

    SOCIAL_AUTH_RDIO_OAUTH1_KEY = ''
    SOCIAL_AUTH_RDIO_OAUTH1_SECRET = ''


OAuth 2.0
---------

To setup Rdio OAuth 2.0, add the following to your settings page::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.rdio.RdioOAuth2',
        ...
    )

    SOCIAL_AUTH_RDIO_OAUTH2_KEY = os.environ['RDIO_OAUTH2_KEY']
    SOCIAL_AUTH_RDIO_OAUTH2_SECRET = os.environ['RDIO_OAUTH2_SECRET']
    SOCIAL_AUTH_RDIO_OAUTH2_SCOPE = []


Extra Fields
------------

The following extra fields are automatically requested:

- rdio_id
- rdio_icon_url
- rdio_profile_url
- rdio_username
- rdio_stream_region
