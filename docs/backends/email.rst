Email Auth
==========

python-social-auth_ comes with an EmailAuth_ backend which comes handy when
your site uses requires the plain old email and password authentication
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

``SOCIAL_AUTH_EMAIL_FORM_URL = '/login-form/'``
    Used to redirect the user to the login/signup form, it must have at least
    one field named ``email``. Form submit should go to ``/complete/email``,
    or if it goes to your view, then your view should complete the process
    calling ``social.actions.do_complete``.

``SOCIAL_AUTH_EMAIL_FORM_HTML = 'login_form.html'``
    The template will be used to render the login/signup form to the user, it
    must have at least one field named ``email``. Form submit should go to
    ``/complete/email``, or if it goes to your view, then your view should
    complete the process calling ``social.actions.do_complete``.


Email validation
----------------

There's a pipeline to validate email addresses, but it relies a lot on your
project.

The pipeline is at ``social.pipeline.mail.mail_validation`` and it's a partial
pipeline, it will return a redirect to an URL that you can use to tell the
users that an email validation was sent to them. If you want to mention the
email address you can get it from the session under the key ``email_validation_address``.

In order to send the validation python-social-auth_ needs a function that will
take care of it, this function is defined by the developer and defined under
the setting ``SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION``. It should be an import
path. This function should take two arguments ``strategy`` and ``code``.
``code`` is a model instance used to validate the email address, it contains
three fields:

``code = '...'``
    Holds an ``uuid.uuid4()`` value and it's the code used to identify the
    validation process.

``email = '...'``
    Email address trying to be validate.

``verified = True / False``
    Flag marking if the email was verified or not.
    
You should use the code in this instance the build the link for email
validation which should go to ``/complete/email?code=<code here>``, if using
Django you can do it with::

    from django.core.urlresolvers import reverse
    url = strategy.build_absolute_uri(
        reverse('social:complete', args=(strategy.backend_name,))
    ) + '?code=' + code.code

On Flask::

    from flask import url_for
    url = url_for('social.complete', backend=strategy.backend_name,
                  _external=True) + '?code=' + code

This pipeline can be used globally with any backend if this setting is
defined::

    SOCIAL_AUTH_FORCE_EMAIL_VALIDATION = True

Or individually by defining the setting per backend basis like
``SOCIAL_AUTH_TWITTER_FORCE_EMAIL_VALIDATION = True``.


Password handling
-----------------

Here's an example of password handling to add to the pipeline::

    def user_password(strategy, user, is_new=False, *args, **kwargs):
        if strategy.backend_name != 'email':
            return

        password = strategy.request_data()['password']
        if is_new:
            user.set_password(password)
            user.save()
        elif not user.validate_password(password):
            # return {'user': None, 'social': None}
            raise AuthException(strategy.backend)

.. _python-social-auth: https://github.com/omab/python-social-auth
.. _EmailAuth: https://github.com/omab/python-social-auth/blob/master/social/backends/email.py#L5
