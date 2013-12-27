Porting from django-social-auth
===============================


Being a derivative work from django-social-auth_, porting from it to
python-social-auth_ should be an easy task. Porting to others libraries usually
is a pain, I'm trying to make this as easy as possible.


Installed apps
--------------

On django-social-auth_ there was a single application to add into
``INSTALLED_APPS`` plus a setting to define which ORM to be used (default or
MongoEngine). Now the apps are split and there's not need for that extra
setting.

When using the default ORM::

    INSTALLED_APPS = (
        ...
        'social.apps.django_app.default',
        ...
    )

And when using MongoEngine::

    INSTALLED_APPS = (
        ...
        'social.apps.django_app.me',
        ...
    )

The models table names were defined to be compatible with those used on
django-social-auth_, so data is not needed to be migrated.


URLs
----

The URLs are namespaced, you can chose your namespace, the `example app`_ uses
the ``social`` namespace. Replace the old include with::

    urlpatterns = patterns('',
        ...
        url('', include('social.apps.django_app.urls', namespace='social'))
        ...
    )

On templates use a namespaced URL::

    {% url social:begin "google-oauth2" %}

Account disconnection URL would be::

    {% url social:disconnect_individual provider, id %}


Porting settings
----------------

All python-social-auth_ settings are prefixed with ``SOCIAL_AUTH_``, except for
some exception on Django framework, ``AUTHENTICATION_BACKENDS`` remains the
same for obvious reasons.

All backends settings have the backend name into it, all uppercase and with
dashes replaced with underscores, take for instance Google OAuth2 backend is
named ``google-oauth2``, any setting name related to that backend should start
with ``SOCIAL_AUTH_GOOGLE_OAUTH2_``.

Keys and secrets are some mandatory settings needed for OAuth providers, to
keep consistency the names follow the same naming convention ``*_KEY`` for the
application key, and ``*_SECRET`` for the secret. OAuth1 backends use to have
``CONSUMER`` in the setting name, not anymore. Following with the Google OAuth2
example::

    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '...'
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '...'

Remember that the name of the backend is needed in the settings, and names
differ a little from backend to backend, like `Facebook OAuth2 backend`_ name
is ``facebook``. So the settings should be::

    SOCIAL_AUTH_FACEBOOK_KEY = '...'
    SOCIAL_AUTH_FACEBOOK_SECRET = '...'


Authentication backends
-----------------------

Import path for authentication backends changed a little, there's no more
``contrib`` module, there's no need for it. Some backends changed the names to
have some consistency, check the backends, it should be easy to track the names
changes. Examples of the new import paths::

    AUTHENTICATION_BACKENDS = (
        'social.backends.open_id.OpenIdAuth',
        'social.backends.google.GoogleOpenId',
        'social.backends.google.GoogleOAuth2',
        'social.backends.google.GoogleOAuth',
        'social.backends.twitter.TwitterOAuth',
        'social.backends.facebook.FacebookOAuth2',
    )


Session
-------

Django stores the last authentication backend used in the user session, this
can cause import troubles when porting since the old import paths aren't valid
anymore. Sadly so far the only solution is to clean the sessions content, that
means to force the user to login again.

.. _django-social-auth: https://github.com/omab/django-social-auth
.. _python-social-auth: https://github.com/omab/python-social-auth
.. _example app: https://github.com/omab/python-social-auth/blob/master/examples/django_example/dj/urls.py#L7
.. _Facebook OAuth2 backend: https://github.com/omab/python-social-auth/blob/master/social/backends/facebook.py#L29
