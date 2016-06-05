Untappd
=======

Untappd uses OAuth v2 for Authentication, check the `official docs`_.

- Create an app by filling out the form here: `Add App`_

- Apps are approved on a one-by-one basis, so you'll need to wait a few days to get your client ID and secret.

- Fill ``Client ID`` and ``Client Secret`` values in the settings::

        SOCIAL_AUTH_UNTAPPD_KEY = '<App UID>'
        SOCIAL_AUTH_UNTAPPD_SECRET = '<App secret>'

- Add the backend to the ``AUTHENTICATION_BACKENDS`` setting::

        AUTHENTICATION_BACKENDS = (
            ...
            'social.backends.untappd.UntappdOAuth2',
            ...
        )

- Then you can start using ``{% url social:begin 'untappd' %}`` in
  your templates

.. _official docs: https://untappd.com/api/docs
.. _Add App: https://untappd.com/api/register?register=new
