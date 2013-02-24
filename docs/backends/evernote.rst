Evernote OAuth
==============

Evernote OAuth 1.0 for its authentication workflow.

- Register a new application at `Evernote API Key form`_.

- Fill ``Consumer Key`` and ``Consumer Secret`` values in the settings::

      SOCIAL_AUTH_EVERNOTE_KEY = ''
      SOCIAL_AUTH_EVERNOTE_SECRET = ''


Sandbox
-------

Evernote supports a sandbox mode for testing, there's a custom backend for it
which name is ``evernote-sandbox`` instead of ``evernote``. Same settings apply
but use these instead::

      SOCIAL_AUTH_EVERNOTE_SANDBOX_KEY = ''
      SOCIAL_AUTH_EVERNOTE_SANDBOX_SECRET = ''

.. _Evernote API Key form: http://dev.evernote.com/support/api_key.php
