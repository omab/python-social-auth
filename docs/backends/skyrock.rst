Skyrock
=======

OAuth based Skyrock Connect.

Skyrock offers per application keys named ``Consumer Key`` and ``Consumer
Secret``. To enable Skyrock these two keys are needed. Further documentation
at `Skyrock developer resources`_:

- Register a new application at `Skyrock App Creation`_,

- Your callback domain should match your application URL in your application
  configuration.

- Fill **Consumer Key** and **Consumer Secret** values::

      SOCIAL_AUTH_SKYROCK_KEY = ''
      SOCIAL_AUTH_SKYROCK_SECRET = ''

.. _Skyrock developer resources: http://www.skyrock.com/developer/
.. _Skyrock App Creation: https://wwwskyrock.com/developer/application
