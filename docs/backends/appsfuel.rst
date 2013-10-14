Appsfuel
========
Appsfuel uses OAuth v2 for Authentication (`Official Docs`_)

- Sign up at the `Appsfuel Developer Program`_

- Create and verify a new app

- On the dashboard click on **Show API keys**

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

      APPSFUEL_CLIENT_ID = '<App UID>'
      APPSFUEL_CLIENT_SECRET = '<App secret>'

Appsfuel gives you the chance to integrate with **Live** or **Sandbox** env.

Appsfuel Live
-------------

- Add 'social.backends.contrib.appsfuel.AppsfuelBackend' into your AUTHENTICATION_BACKENDS.

- Then you can start using {% url social:begin 'appsfuel' %} in your templates

Appsfuel Sandbox
----------------

- Add 'social.backends.contrib.appsfuel.AppsfuelSandboxBackend' into your AUTHENTICATION_BACKENDS.

- Then you can start using {% url social:begin 'appsfuel-sandbox' %} in your templates


.. _Official Docs: http://docs.appsfuel.com/api_reference#api_integration
.. _Appsfuel Developer Program: https://developer.appsfuel.com

