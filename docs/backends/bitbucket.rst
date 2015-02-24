Bitbucket
=========

Bitbucket works similar to Twitter OAuth.

- Register a new application by emailing ``support@bitbucket.org`` with an
  application name and a bit of a description,

- Fill ``Consumer Key`` and ``Consumer Secret`` values in the settings::

      SOCIAL_AUTH_BITBUCKET_KEY = ''
      SOCIAL_AUTH_BITBUCKET_SECRET = ''



Settings
--------

Sometimes Bitbucket users don't have a verified email address, making it
impossible to get the basic user information to continue the auth process.
It's possible to avoid these users with this setting::

    SOCIAL_AUTH_BITBUCKET_VERIFIED_EMAILS_ONLY = True

By default the setting is set to ``False`` since it's possible for a project to
gather this information by other methods.
