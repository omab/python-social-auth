Dropbox
=======

Dropbox supports both OAuth 1 and 2.

- Register a new application at `Dropbox Developers`_, and follow the
  instructions below for the version of OAuth for which you are adding
  support.


OAuth2 Api V2
------

Add the Dropbox OAuth2 backend to your settings page::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.dropbox.DropboxOAuth2V2',
        ...
    )

- Fill ``App Key`` and ``App Secret`` values in the settings::

      SOCIAL_AUTH_DROPBOX_OAUTH2_KEY = ''
      SOCIAL_AUTH_DROPBOX_OAUTH2_SECRET = ''

OAuth1
------

.. deprecated:: V1 api is deprecated.
https://blogs.dropbox.com/developers/2016/06/api-v1-deprecated/
Add the Dropbox OAuth backend to your settings page::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.dropbox.DropboxOAuth',
        ...
    )

- Fill ``App Key`` and ``App Secret`` values in the settings::

      SOCIAL_AUTH_DROPBOX_KEY = ''
      SOCIAL_AUTH_DROPBOX_SECRET = ''

OAuth2
------

.. deprecated:: V1 api is deprecated.
https://blogs.dropbox.com/developers/2016/06/api-v1-deprecated/

Add the Dropbox OAuth2 backend to your settings page::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.dropbox.DropboxOAuth2',
        ...
    )

- Fill ``App Key`` and ``App Secret`` values in the settings::

      SOCIAL_AUTH_DROPBOX_OAUTH2_KEY = ''
      SOCIAL_AUTH_DROPBOX_OAUTH2_SECRET = ''

.. _Dropbox Developers: https://www.dropbox.com/developers/apps
