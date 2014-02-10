Flask Framework
===============

Flask reusable applications are tricky (or I'm not capable enough). Here are
details on how to enable this application on Flask.


Dependencies
------------

The `Flask built-in app` depends on sqlalchemy_, there's no support for others
ORMs yet but pull-requests are welcome.


Enabling the application
------------------------

The application defines a `Flask Blueprint`_, which needs to be registered once
the Flask app is configured::

    from social.apps.flask_app.routes import social_auth

    app.register_blueprint(social_auth)


Models Setup
------------

At the moment the models for python-social-auth_ are defined inside a function
because they need the reference to the current db instance and the User model
used on your project (check *User model reference* below). Once the Flask app
and the database are defined, call ``init_social`` to register the models::

    from social.apps.flask_app.models import init_social

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


.. _Flask Blueprint: http://flask.pocoo.org/docs/blueprints/
.. _Flask-Login: https://github.com/maxcountryman/flask-login
.. _python-social-auth: https://github.com/omab/python-social-auth
.. _Flask built-in app: https://github.com/omab/python-social-auth/tree/master/social/apps/flask_app
.. _sqlalchemy: http://www.sqlalchemy.org/
