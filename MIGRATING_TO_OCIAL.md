# Migrating from python-social-auth to split social

Since Dec 03 2016, [python-social-auth](https://github.com/omab/python-social-auth)
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
frameworks also need to define their corresponding requirement, or use
one of the defined `extras` in the `setup.py` file.

## Django

Django users need to add the `social-auth-app-django`
dependency. Those using `mongoengine`, need to add
`social-auth-app-mongoengine`.

### Migrations

Several errors were reported due to migrations not applying properly
when migrating to the new app, most of them are caused because the app
switched names a few times, from `default` to `social_auth`, and
probably something else in between. That's the reason the migrations
define the `replaces` attribute, that way Django can identify already
applied migrations and not run them again.

In order to make complete the move to the new project setup, first
ensure to move to `python-social-auth==0.2.21`, run the migrations at
that point, then continue with the move to the new project and run the
migrations again. Steps:

1. Update to `0.2.21`
   ```
   pip install "python-social-auth==0.2.21"
   ```

2. Run migrations
   ```
   python manage.py migrate
   ```

3. Move to the new project

4. Run migrations again
   ```
   python manage.py migrate
   ```

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
- Update your urls patterns to include `'social_django.urls'` instead of
  `'social.apps.django_app.urls'`.

### Extras supported

```
$ pip install python-social-auth[django]
$ pip install python-social-auth[django-mongoengine]
```

## Flask

Flask users need to add `social-auth-app-flask`, and depending on the
storage solution, add one of the following too:

  - `social-auth-app-flask-sqlalchemy` when using SQLAlchemy
  - `social-auth-app-flask-mongoengine` when using Mongoengine
  - `social-auth-app-flask-peewee` when using Peewee


### Extras supported

```
$ pip install python-social-auth[flask]
$ pip install python-social-auth[flask-mongoengine]
$ pip install python-social-auth[flask-peewee]
```

## Pyramid

Pyramid users need to add `social-auth-app-pyramid` to their dependencies.

### Extras supported

```
$ pip install python-social-auth[pyramid]
```

## Tornado

Tornado users need to add `social-auth-app-tornado` to their dependencies.

### Extras supported

```
$ pip install python-social-auth[tornado]
```


## Webpy

Web.py users need to add `social-auth-app-webpy` to their dependencies.

### Extras supported

```
$ pip install python-social-auth[webpy]
```


## Cherrypy

Cherrypy users need to add `social-auth-app-cherrypy` to their dependencies.

### Extras supported

```
$ pip install python-social-auth[cherrypy]
```
