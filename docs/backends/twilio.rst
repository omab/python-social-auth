Twilio
======

- Register a new application at `Twilio Connect Api`_

- Fill ``SOCIAL_AUTH_TWILIO_KEY`` and ``SOCIAL_AUTH_TWILIO_SECRET`` values in
  the settings::

    SOCIAL_AUTH_TWILIO_KEY = ''
    SOCIAL_AUTH_TWILIO_SECRET = ''

- Add desired authentication backends to Django's ``SOCIAL_AUTH_AUTHENTICATION_BACKENDS``
  setting::

    'social.backends.twilio.TwilioAuth',

- Usage example::

    <a href="/login/twilio">Enter using Twilio</a>


.. _Twilio Connect API: https://www.twilio.com/user/account/connect/apps
