Django Framework
================

Django framework has a little more support since this application was derived
from `django-social-auth`_. Here are some details on configuring this
application on Django.


Register the application
------------------------

The `Django built-in app`_ comes with two ORMs, one for default Django ORM and
another for MongoEngine_ ORM.

Add the application to ``INSTALLED_APPS`` setting, for default ORM::

    INSTALLED_APPS = (
        ...
        'social.apps.django_app.default',
        ...
    )

And for MongoEngine_ ORM::

    INSTALLED_APPS = (
        ...
        'social.apps.django_app.me',
        ...
    )

Also ensure to define the MongoEngine_ storage setting::

    SOCIAL_AUTH_STORAGE = 'social.apps.django_app.me.models.DjangoStorage'


Database
--------

(For Django 1.7 and higher) sync database to create needed models::

    ./manage.py makemigrations



Sync database to create needed models::

    ./manage.py syncdb


Authentication backends
-----------------------

Add desired authentication backends to Django's AUTHENTICATION_BACKENDS_
setting::

    AUTHENTICATION_BACKENDS = (
        'social.backends.open_id.OpenIdAuth',
        'social.backends.google.GoogleOpenId',
        'social.backends.google.GoogleOAuth2',
        'social.backends.google.GoogleOAuth',
        'social.backends.twitter.TwitterOAuth',
        'social.backends.yahoo.YahooOpenId',
        ...
        'django.contrib.auth.backends.ModelBackend',
    )

Take into account that backends **must** be defined in AUTHENTICATION_BACKENDS_
or Django won't pick them when trying to authenticate the user.

Don't miss ``django.contrib.auth.backends.ModelBackend`` if using ``django.contrib.auth``
application or users won't be able to login by username / password method.


URLs entries
------------

Add URLs entries::

    urlpatterns = patterns('',
        ...
        url('', include('social.apps.django_app.urls', namespace='social'))
        ...
    )

In case you need a custom namespace, this setting is also needed::

    SOCIAL_AUTH_URL_NAMESPACE = 'social'


Template Context Processors
---------------------------

There's a context processor that will add backends and associations data to
template context::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'social.apps.django_app.context_processors.backends',
        'social.apps.django_app.context_processors.login_redirect',
        ...
    )

``backends`` context processor will load a ``backends`` key in the context with
three entries on it:

``associated``
    It's a list of ``UserSocialAuth`` instances related with the currently
    logged in user. Will be empty if there's no current user.

``not_associated``
    A list of available backend names not associated with the current user yet.
    If there's no user logged in, it will be a list of all available backends.

``backends``
    A list of all available backend names.


ORMs
----

As detailed above the built-in Django application supports default ORM and
MongoEngine_ ORM.

When using MongoEngine_ make sure you've followed the instructions for
`MongoEngine Django integration`_, as you're now utilizing that user model. The
`MongoEngine_` backend was developed and tested with version 0.6.10 of
`MongoEngine_`.

Alternate storage models implementations currently follow a tight pattern of
models that behave near or identical to Django ORM models. It is currently
not decoupled from this pattern by any abstraction layer. If you would like
to implement your own alternate, please see the
``social.apps.django_app.default.models`` and
``social.apps.django_app.me.models`` modules for guidance.


Exceptions Middleware
---------------------

A base middleware is provided that handles ``SocialAuthBaseException`` by
providing a message to the user via the Django messages framework, and then
responding with a redirect to a URL defined in one of the middleware methods.

The middleware is at ``social.apps.django_app.middleware.SocialAuthExceptionMiddleware``. 
Any method can be overrided but for simplifications these two are the
recommended::

    get_message(request, exception)
    get_redirect_uri(request, exception)

By default, the message is the exception message and the URL for the redirect
is the location specified by the ``LOGIN_ERROR_URL`` setting.

If a valid backend was detected by ``strategy()`` decorator, it will be
available at ``request.strategy.backend`` and ``process_exception()`` will
use it to build a backend-dependent redirect URL but fallback to default if not
defined.

Exception processing is disabled if any of this settings is defined with a
``True`` value::

    <backend name>_SOCIAL_AUTH_RAISE_EXCEPTIONS = True
    SOCIAL_AUTH_RAISE_EXCEPTIONS = True
    RAISE_EXCEPTIONS = True
    DEBUG = True

The redirect destination will get two ``GET`` parameters:

``message = ''``
    Message from the exception raised, in some cases it's the message returned
    by the provider during the auth process.

``backend = ''``
    Backend name that was used, if it was a valid backend.


Django Admin
------------

The default application (not the MongoEngine_ one) contains an ``admin.py``
module that will be auto-discovered by the usual mechanism.

But, by the nature of the application which depends on the existence of a user
model, it's easy to fall in a recursive import ordering making the application
fail to load. This happens because the admin module will build a set of fields
to populate the ``search_fields`` property to search for related users in the
administration UI, but this requires the user model to be retrieved which might
not be defined at that time.

To avoid this issue define the following setting to circumvent the import
error::

    SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['field1', 'field2']

For example::

    SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']

The fields listed **must** be user models fields.

.. _MongoEngine: http://mongoengine.org
.. _MongoEngine Django integration: http://mongoengine-odm.readthedocs.org/en/latest/django.html
.. _django-social-auth: https://github.com/omab/django-social-auth
.. _Django built-in app: https://github.com/omab/python-social-auth/tree/master/social/apps/django_app
.. _AUTHENTICATION_BACKENDS: http://docs.djangoproject.com/en/dev/ref/settings/?from=olddocs#authentication-backends
.. _django@dc43fbc: https://github.com/django/django/commit/dc43fbc2f21c12e34e309d0e8a121020391aa03a
