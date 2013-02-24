Angel List
==========

Angel uses OAuth v2 for Authentication.

- Register a new application at the `Angel List API`_, and

- fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_ANGEL_KEY = ''
      SOCIAL_AUTH_ANGEL_SECRET = ''

- extra scopes can be defined by using::

    SOCIAL_AUTH_ANGEL_AUTH_EXTRA_ARGUMENTS = {'scope': 'email messages'}

**Note:**
Angel List does not currently support returning ``state`` parameter used to
validate the auth process.

.. _Angel List API: https://angel.co/api/oauth/faq
