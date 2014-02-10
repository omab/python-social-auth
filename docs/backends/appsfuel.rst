Appsfuel
========

Appsfuel uses OAuth v2 for Authentication check the `official docs`_ too.

- Sign up at the `Appsfuel Developer Program`_

- Create and verify a new app

- On the dashboard click on **Show API keys**

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_APPSFUEL_KEY = '<App UID>'
      SOCIAL_AUTH_APPSFUEL_SECRET = '<App secret>'

Appsfuel gives you the chance to integrate with **Live** or **Sandbox** env.


Appsfuel Live
-------------

- Add 'social.backends.contrib.appsfuel.AppsfuelBackend' into your
  ``AUTHENTICATION_BACKENDS``.

- Then you can start using ``{% url social:begin 'appsfuel' %}`` in your
  templates


Appsfuel Sandbox
----------------

- Add ``'social.backends.appsfuel.AppsfuelOAuth2Sandbox'`` into your
  ``AUTHENTICATION_BACKENDS``.

- Then you can start using ``{% url social:begin 'appsfuel-sandbox' %}`` in
  your templates

- Define the settings::

    SOCIAL_AUTH_APPSFUEL_SANDBOX_KEY = '<App UID>'
    SOCIAL_AUTH_APPSFUEL_SANDBOX_SECRET = '<App secret>'


.. _official docs: http://docs.appsfuel.com/api_reference#api_integration
.. _Appsfuel Developer Program: https://developer.appsfuel.com
