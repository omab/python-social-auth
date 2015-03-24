Khan Academy
============

Khan Academy uses a variant of OAuth1 authentication flow. Check the API
details at `Khan Academy API Authentication`_.

Follow this steps in order to use the backend:

- Register a new application at `Khan Academy API Apps`_,

- Fill **Consumer Key** and **Consumer Secret** values::

    SOCIAL_AUTH_KHANACADEMY_OAUTH1_KEY = ''
    SOCIAL_AUTH_KHANACADEMY_OAUTH1_SECRET = ''

- Add the backend to ``AUTHENTICATION_BACKENDS`` setting::

    AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.khanacademy.KhanAcademyOAuth1',
        ...
    )

.. _Khan Academy API Authentication: https://github.com/Khan/khan-api/wiki/Khan-Academy-API-Authentication
.. _Khan Academy API Apps: http://www.khanacademy.org/api-apps/register
