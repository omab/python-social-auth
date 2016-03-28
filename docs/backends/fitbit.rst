Fitbit
======

Fitbit supports both OAuth 2.0 and OAuth 1.0a logins.
OAuth 2 is preferred for new integrations, as OAuth 1.0a does not support getting heartrate or location and will be deprecated in the future.

1. Register a new OAuth Consumer `here`_

2. Configure the appropriate settings for OAuth 2.0 or OAuth 1.0a (see below).

OAuth 2.0 or OAuth 1.0a
-----------------------

- Fill ``Consumer Key`` and ``Consumer Secret`` values in the settings::

    SOCIAL_AUTH_FITBIT_KEY = '<your-consumer-key>'
    SOCIAL_AUTH_FITBIT_SECRET = '<your-consumer-secret>'

OAuth 2.0 specific settings
---------------------------

By default, only the ``profile`` scope is requested. To request more scopes, set SOCIAL_AUTH_FITBIT_SCOPE::

    SOCIAL_AUTH_FITBIT_SCOPE = [
      'activity',
      'heartrate',
      'location',
      'nutrition',
      'profile',
      'settings',
      'sleep',
      'social',
      'weight'
    ]

The above will request all permissions from the user.

.. _here: https://dev.fitbit.com/apps/new
