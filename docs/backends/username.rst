Username Auth
=============

python-social-auth_ comes with an UsernameAuth_ backend which comes handy when
your site uses requires the plain old username and password authentication
mechanism.

Actually that's a lie since the backend doesn't handle password at all, that's
up to the developer to validate the password in and the proper place to do it
is the pipeline, right after the user instance was retrieved or created.

The reason to leave password handling to the developer is because too many
things are really tied to the project, like the field where the password is
stored, salt handling, password hashing algorithm and validation. So just add
the pipeline functions that will do that following the needs of your project.


Backend settings
----------------

``SOCIAL_AUTH_USERNAME_FORM_URL = '/login-form/'``
    Used to redirect the user to the login/signup form, it must have at least
    one field named ``username``. Form submit should go to ``/complete/username``,
    or if it goes to your view, then your view should complete the process
    calling ``social.actions.do_complete``.

``SOCIAL_AUTH_USERNAME_FORM_HTML = 'login_form.html'``
    The template will be used to render the login/signup form to the user, it
    must have at least one field named ``username``. Form submit should go to
    ``/complete/username``, or if it goes to your view, then your view should
    complete the process calling ``social.actions.do_complete``.


Password handling
-----------------

Here's an example of password handling to add to the pipeline::

    def user_password(strategy, user, is_new=False, *args, **kwargs):
        if strategy.backend.name != 'username':
            return

        password = strategy.request_data()['password']
        if is_new:
            user.set_password(password)
            user.save()
        elif not user.validate_password(password):
            # return {'user': None, 'social': None}
            raise AuthException(strategy.backend)

.. _python-social-auth: https://github.com/omab/python-social-auth
.. _UsernameAuth: https://github.com/omab/python-social-auth/blob/master/social/backends/username.py#L5
