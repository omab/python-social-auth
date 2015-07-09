Bitbucket
=========

Bitbucket supports both OAuth2 and OAuth1 logins.

1. Register a new OAuth Consumer by following the instructions in the
   Bitbucket documentation: `OAuth on Bitbucket`_

   Note: For OAuth2, your consumer MUST have the "account" scope otherwise
   the user profile information (username, name, etc.) won't be accessible.

2. Configure the appropriate settings for OAuth2 or OAuth1 (see below).


OAuth2
------

- Fill ``Consumer Key`` and ``Consumer Secret`` values in the settings::

    SOCIAL_AUTH_BITBUCKET_OAUTH2_KEY = '<your-consumer-key>'
    SOCIAL_AUTH_BITBUCKET_OAUTH2_SECRET = '<your-consumer-secret>'

- If you would like to restrict access to only users with verified e-mail
  addresses, set ``SOCIAL_AUTH_BITBUCKET_OAUTH2_VERIFIED_EMAILS_ONLY = True``
  By default the setting is set to ``False`` since it's possible for a
  project to gather this information by other methods.

  
OAuth1
------

- OAuth1 works similarly to OAuth2, but you must fill in the following settings
  instead::

    SOCIAL_AUTH_BITBUCKET_KEY = '<your-consumer-key>'
    SOCIAL_AUTH_BITBUCKET_SECRET = '<your-consumer-secret>'

- If you would like to restrict access to only users with verified e-mail
  addresses, set ``SOCIAL_AUTH_BITBUCKET_VERIFIED_EMAILS_ONLY = True``.
  By default the setting is set to ``False`` since it's possible for a
  project to gather this information by other methods.


User ID
-------

Bitbucket recommends the use of UUID_ as the user identifier instead
of ``username`` since they can change and impose a security risk. For
that reason ``UUID`` is used by default, but for backward
compatibility reasons, it's possible to get the old behavior again by
defining this setting::

    SOCIAL_AUTH_BITBUCKET_USERNAME_AS_ID = True

.. _UUID: https://confluence.atlassian.com/display/BITBUCKET/Use+the+Bitbucket+REST+APIs
.. _OAuth on Bitbucket: https://confluence.atlassian.com/display/BITBUCKET/OAuth+on+Bitbucket
