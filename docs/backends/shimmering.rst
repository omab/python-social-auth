Shimmering Verify
=================

Shimmering implemented OAuth2 protocol for their authentication mechanism. To
enable ``python-social-auth`` support follow this steps:

1. Go to `Shimmering Developer Console`_ and create an application.

2. Fill App Id and Secret in your project settings::

    SOCIAL_AUTH_SHIMMERING_KEY = '...'
    SOCIAL_AUTH_SHIMMERING_SECRET = '...'

3. Enable the backend::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.shimmering.ShimmeringOAuth2',
        ...
    )

.. _Shimmering Developer Console: http://developers.shimmeringverify.com