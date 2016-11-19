MailChimp
=======

MailChimp uses OAuth v2 for Authentication, check the `official docs`_.

- Create an app by filling out the form here: `Add App`_

- Fill ``Client ID`` and ``Client Secret`` values in the settings::

        SOCIAL_AUTH_MAILCHIMP_KEY = '<App UID>'
        SOCIAL_AUTH_MAILCHIMP_SECRET = '<App secret>'

- Add the backend to the ``AUTHENTICATION_BACKENDS`` setting::

        AUTHENTICATION_BACKENDS = (
            ...
            'social.backends.mailchimp.MailChimpOAuth2',
            ...
        )

- Then you can start using ``{% url social:begin 'mailchimp' %}`` in
  your templates

.. _official docs: https://apidocs.mailchimp.com/oauth2/
.. _Add App: https://admin.mailchimp.com/account/oauth2/
