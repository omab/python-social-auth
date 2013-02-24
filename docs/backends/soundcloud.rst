SoundCloud
==========

SoundCloud uses OAuth2 for its auth mechanism.

- Register a new application at `SoundCloud App Registration`_, set your
  application name, website and redirect URI.

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_SOUNDCLOUD_KEY = ''
      SOCIAL_AUTH_SOUNDCLOUD_SECRET = ''

- Also it's possible to define extra permissions with::

     SOCIAL_AUTH_SOUNDCLOUD_SCOPE = [...]

Possible scope values are `*` or `non-expiring` according to their `/connect
documentation`_.

Check the rest of their doc at `SoundCloud Developer Documentation`_.

.. _SoundCloud App Registration: http://soundcloud.com/you/apps/new
.. _SoundCloud Developer Documentation: http://developers.soundcloud.com/docs
.. _/connect documentation: http://developers.soundcloud.com/docs/api/reference#connect
