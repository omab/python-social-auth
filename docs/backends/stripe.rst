Stripe
======

Stripe uses OAuth2 for its authorization service. To setup Stripe backend:

- Register a new application at `Stripe App Creation`_, and

- Grab the ``client_id`` value in ``Applications`` tab and fill the ``App Id``
  setting::

    SOCIAL_AUTH_STRIPE_KEY = 'ca_...'

- Grab the ``Test Secret Key`` in the ``API Keys`` tab and fille the ``App
  Secret`` setting::

    SOCIAL_AUTH_STRIPE_SECRET = '...'

- Define ``SOCIAL_AUTH_STRIPE_SCOPE`` with the desired scope (options are
  ``read_only`` and ``read_write``)::

    SOCIAL_AUTH_STRIPE_SCOPE = ['read_only']

- Add the needed backend to ``SOCIAL_AUTH_AUTHENTICATION_BACKENDS``::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.stripe.StripeOAuth2',
        ...
    )

More info on Stripe OAuth2 at `Integrating OAuth`_.

.. _Stripe App Creation: https://manage.stripe.com/#account/applications/settings
.. _Integrating OAuth: https://stripe.com/docs/connect/oauth
