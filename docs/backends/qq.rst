QQ
==

QQ implemented OAuth2 protocol for their authentication mechanism. To enable
``python-social-auth`` support follow this steps:

1. Go to `QQ`_ and create an application.

2. Fill App Id and Secret in your project settings::

    SOCIAL_AUTH_QQ_KEY = '...'
    SOCIAL_AUTH_QQ_SECRET = '...'

3. Enable the backend::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.qq.QQOauth2',
        ...
    )


The values for ``nickname``, ``figureurl_qq_1`` and ``gender`` will be stored
in the ``extra_data`` field. The ``nickname`` will be used as the account
username. ``figureurl_qq_1`` can be used as the profile image.

.. _QQ: http://connect.qq.com/
