Coursera
============

Coursera uses a variant of OAuth2 authentication. The details of the API
can be found at `OAuth2-based APIs - Coursera Technology`_.

Take the following steps in order to use the backend:

1. Create an account at `Coursera`_.

2. Open `Developer Console`_, create an organisation and application.

3. Set **Client ID** as a ``SOCIAL_AUTH_COURSERA_KEY`` and
**Secret Key** as a ``SOCIAL_AUTH_COURSERA_SECRET`` in your local settings.

4. Add the backend to ``AUTHENTICATION_BACKENDS`` setting::

    AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.coursera.CourseraOAuth2',
        ...
    )

.. _OAuth2-based APIs - Coursera Technology: https://tech.coursera.org/app-platform/oauth2/
.. _Coursera: https://accounts.coursera.org/console
.. _Developer Console: https://accounts.coursera.org/console
