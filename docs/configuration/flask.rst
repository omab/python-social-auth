Flask Framework
===============

Flask reusable applications are tricky (or I'm not capable enough). Here are
details on how to enable this application on Flask.


Dependencies
------------

The `Flask built-in app` depends on sqlalchemy_, there's initial support for
MongoEngine_ ORM too (check below for more details).


Enabling the application
------------------------

The applications define a `Flask Blueprint`_, which needs to be registered once
the Flask app is configured by::

    from social.apps.flask_app.routes import social_auth

    app.register_blueprint(social_auth)

For MongoEngine_ you need this setting::

    SOCIAL_AUTH_STORAGE = 'social.apps.flask_app.me.models.FlaskStorage'


Models Setup
------------

At the moment the models for python-social-auth_ are defined inside a function
because they need the reference to the current db instance and the User model
used on your project (check *User model reference* below). Once the Flask app
and the database are defined, call ``init_social`` to register the models::

    from social.apps.flask_app.default.models import init_social

    init_social(app, db)

For MongoEngine_::

    from social.apps.flask_app.me.models import init_social

    init_social(app, db)

So far I wasn't able to find another way to define the models on another way
rather than making it as a side-effect of calling this function since the
database is not available and ``current_app`` cannot be used on init time, just
run time.


User model reference
--------------------

The application keeps a reference to the User model used by your project,
define it by using this setting::

    SOCIAL_AUTH_USER_MODEL = 'foobar.models.User'

The value must be the import path to the User model.


Global user
-----------

The application expects the current logged in user accesible at ``g.user``,
define a handler like this to ensure that::

    @app.before_request
    def global_user():
        g.user = get_current_logged_in_user


Flask-Login
-----------

The application works quite well with Flask-Login_, ensure to have some similar
handlers to these::

    @login_manager.user_loader
    def load_user(userid):
        try:
            return User.query.get(int(userid))
        except (TypeError, ValueError):
            pass


    @app.before_request
    def global_user():
        g.user = login.current_user


    # Make current user available on templates
    @app.context_processor
    def inject_user():
        try:
            return {'user': g.user}
        except AttributeError:
            return {'user': None}


Remembering sessions
--------------------

The users session can be remembered when specified on login. The common
implementation for this feature is to pass a parameter from the login form
(``remember_me``, ``keep``, etc), to flag the action. Flask-Login_ will mark
the session as persistent if told so.

python-social-auth_ will check for a given name (``keep``) by default, but
since providers won't pass parameters back to the application, the value must
be persisted in the session before the authentication process happens.

So, the following setting is required for this to work::

    SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['keep']

It's possible to override the default name with this setting::

    SOCIAL_AUTH_REMEMBER_SESSION_NAME = 'remember_me'

Don't use the value ``remember`` since that will clash with Flask-Login_ which
pops the value from the session.

Then just pass the parameter ``keep=1`` as a GET or POST parameter.


Exceptions handling
-------------------

The Django application has a middleware (that fits in the framework
architecture) to facilitate the different exceptions_ handling raised by
python-social-auth_. The same can be accomplished (even on a simpler way) in
Flask by defining an errorhandler_. For example the next code will redirect any
social-auth exception to a ``/socialerror`` URL::

    from social.exceptions import SocialAuthBaseException


    @app.errorhandler(500)
    def error_handler(error):
        if isinstance(error, SocialAuthBaseException):
            return redirect('/socialerror')


Be sure to set your debug and test flags to ``False`` when testing this on your
development environment, otherwise the exception will be raised and error
handlers won't be called.


.. _Flask Blueprint: http://flask.pocoo.org/docs/blueprints/
.. _Flask-Login: https://github.com/maxcountryman/flask-login
.. _python-social-auth: https://github.com/omab/python-social-auth
.. _Flask built-in app: https://github.com/omab/python-social-auth/tree/master/social/apps/flask_app
.. _sqlalchemy: http://www.sqlalchemy.org/
.. _exceptions: https://github.com/omab/python-social-auth/blob/master/social/exceptions.py
.. _errorhandler: http://flask.pocoo.org/docs/api/#flask.Flask.errorhandler
.. _MongoEngine: http://mongoengine.org
