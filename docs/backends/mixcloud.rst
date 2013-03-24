Mixcloud OAuth2
===============

The `Mixcloud API`_ offers support for authorization. To this backend support:

- Register a new application at `Mixcloud Developers`_

- Add Mixcloud backend to ``AUTHENTICATION_BACKENDS`` in settings::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.mixcloud.MixcloudOAuth2',
    )

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

    SOCIAL_AUTH_MIXCLOUD_KEY = ''
    SOCIAL_AUTH_MIXCLOUD_SECRET = ''

- Similar to the other OAuth backends you can define::

    SOCIAL_AUTH_MIXCLOUD_EXTRA_DATA = [('username', 'username'),
                                       ('name', 'name'),
                                       ('pictures', 'pictures'),
                                       ('url', 'url')]

  as a list of tuples ``(response name, alias)`` to store user profile data on
  the ``UserSocialAuth.extra_data``.

.. _Mixcloud API: http://www.mixcloud.com/developers/documentation
.. _Mixcloud Developers: http://www.mixcloud.com/developers
