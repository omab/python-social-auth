# Migrating from python-social-auth to split social

Since Dec 03 2016, [python-socia-auth](https://github.com/omab/python-social-auth)
is marked as deprecated and the community is recommended to migrate
towards the packages created in the [organization repository](https://github.com/python-social-auth/social-core).

The new organization split the monolithic structure into smaller
packages with their responsibility well defined, and better
dependencies handling.

Since [v0.3.0](https://github.com/omab/python-social-auth/tree/v0.3.0),
python-social-auth cleaned up the code and added the needed imports to
the new libraries and defined a single dependency in the [requirements.txt](https://github.com/omab/python-social-auth/blob/v0.3.0/requirements.txt)
file, `social-auth-core`, this aims to ease the transition to the new structure.

But that won't solve everybody situation, people using the different
frameworks also need to define their corresponding requirement.

## Django

Django users need to add the `social-auth-app-django`
dependency. Those using `mongoengine`, need to add
`social-auth-app-mongoengine`.

### Settings

- Update your references to `social.*` in your settings, most notably:
  - `AUTHENTICATION_BACKENDS` are now under `social_core.*`
    (e.g. `social_core.backends.facebook.FacebookOAuth2`).
  - Context processors are now under `social_django`
    (e.g. `social_django.context_processors.backends`).
  - `MIDDLEWARE_CLASSES` are now under `social_django`
    (e.g. `social_django.middleware.SocialAuthExceptionMiddleware`).
  - If you have it overridden, `SOCIAL_AUTH_PIPELINE` setting.
- Update your `INSTALLED_APPS` to include `social_django` instead of
`social.apps.django_app.default`.

## Flask

Flask users need to add `social-auth-app-flask`, and depending on the
storage solution, add one of the following too:

  - `social-auth-app-flask-sqlalchemy` when using SQLAlchemy
  - `social-auth-app-flask-mongoengine` when using Mongoengine
  - `social-auth-app-flask-peewee` when using Peewee

## Pyramid

Pyramid users need to add `social-auth-app-pyramid` to their dependencies.

## Tornado

Tornado users need to add `social-auth-app-tornado` to their dependencies.

## Webpy

Web.py users need to add `social-auth-app-webpy` to their dependencies.
