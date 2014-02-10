Webpy Framework
===============

Webpy_ framework is easy to setup, once that python-social-auth_ is installed
or accessible in the ``PYTHONPATH``, just add the needed configurations to make
it run.


Dependencies
------------

The `Webpy built-in app` depends on sqlalchemy_, there's no support for others
ORMs yet but pull-requests are welcome.


Configuration
-------------

Add the needed settings into ``web.config`` store. Settings are prefixed with
``SOCIAL_AUTH_`` but there's a helper for it::

    from social.utils import setting_name

    web.config[setting_name('USER_MODEL')] = 'models.User'
    web.config[setting_name('LOGIN_REDIRECT_URL')] = '/done/'
    web.config[setting_name('AUTHENTICATION_BACKENDS')] = (
        'social.backends.google.GoogleOAuth2',
        ...
    )

Add all the settings needed for the app (check Configuration_ section for
details).


URLs
----

Add the social application into URLs::

    from social.apps.webpy_app import app as social_app

    urls = (
        ...
        '', social_app.app_social
        ...
    )


Session
-------

python-social-auth_ depends on sessions storage to keep some essential values,
usually redirects and ``state`` parameters used to validate authentication
process on OAuth providers.

The `Webpy built-in app` expects the session reference to be available under
``web.web_session`` so ensure it's available there.


User model
----------

Like the other apps, the User model must be defined on settings since
a reference to it is kept on ``UserSocialAuth`` instance. Define like this::

    web.config[setting_name('USER_MODEL')] = 'models.User'

Where the value is the import path to the User model used on your project.


.. _python-social-auth: https://github.com/omab/python-social-auth
.. _Webpy: http://webpy.org/
.. _Webpy built-in app: https://github.com/omab/python-social-auth/tree/master/social/apps/webpy_app
.. _sqlalchemy: http://www.sqlalchemy.org/
