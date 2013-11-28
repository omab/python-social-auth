Fitbit
======

Fitbit offers OAuth1 as their auth mechanism. In order to enable it, follow:

- Register a new application at `Fitbit dev portal`_, be sure to select
  ``Browser`` as the application type. Set the ``Callback URL`` to
  ``http://<your hostname>//complete/fitbit/``.

- Fill **Consumer Key** and **Consumer Secret** values::

      SOCIAL_AUTH_FITBIT_KEY = ''
      SOCIAL_AUTH_FITBIT_SECRET = ''

.. _Fitbit dev portal: https://dev.fitbit.com/apps/new
