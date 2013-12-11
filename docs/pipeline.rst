Pipeline
========

python-social-auth_ uses an extendible pipeline mechanism where developers can
introduce their functions during the authentication, association and
disconnection flows.

The functions will receive a variable set of arguments related to the current
process, common arguments are the current ``strategy``, ``user`` (if any) and
``request``. It's recommended that all the function also define an ``**kwargs``
in the parameters to avoid errors for unexpected arguments.

Each pipeline entry can return a ``dict`` or ``None``, any other type of return
value is treated as a response instance and returned directly to the client,
check *Partial Piepeline* below for details.

If a ``dict`` is returned, the value in the set will be merged into the
``kwargs`` argument for the next pipeline entry, ``None`` is taken as if ``{}``
was returned.


Authentication Pipeline
-----------------------

The final process of the authentication workflow is handled by an operations
pipeline where custom functions can be added or default items can be removed to
provide a custom behavior. The default pipeline is a mechanism that creates
user instances and gathers basic data from providers.

The default pipeline is composed by::

    (
        'social.pipeline.social_auth.social_details',                                                                       
        'social.pipeline.social_auth.social_uid',
        'social.pipeline.social_auth.auth_allowed',
        'social.pipeline.social_auth.social_user',
        'social.pipeline.user.get_username',
        'social.pipeline.user.create_user',
        'social.pipeline.social_auth.associate_user',
        'social.pipeline.social_auth.load_extra_data',
        'social.pipeline.user.user_details'
    )

It's possible to override it by defining the setting ``SOCIAL_AUTH_PIPELINE``,
for example a pipeline that won't create users, just accept already registered
ones would look like this::

    SOCIAL_AUTH_PIPELINE = (
        'social.pipeline.social_auth.social_user',
        'social.pipeline.social_auth.associate_user',
        'social.pipeline.social_auth.load_extra_data',
        'social.pipeline.user.user_details'
    )

Note that this assumes the user is already authenticated, and thus the ``user`` key 
in the dict is populated. In cases where the authentication is purely external, a
pipeline method must be provided that populates the ``user`` key. Example::


    SOCIAL_AUTH_PIPELINE = (
        'myapp.pipeline.load_user',
        'social.pipeline.social_auth.social_user',
        'social.pipeline.social_auth.associate_user',
        'social.pipeline.social_auth.load_extra_data',
        'social.pipeline.user.user_details',
    )

Each pipeline function will receive the following parameters:
    * Current strategy (which gives access to current store, backend and request)
    * User ID given by authentication provider
    * User details given by authentication provider
    * ``is_new`` flag (initialized as ``False``)
    * Any arguments passed to ``auth_complete`` backend method, default views
      pass these arguments:
      - current logged in user (if it's logged in, otherwise ``None``)
      - current request


Disconnection Pipeline
----------------------

Like the authentication pipeline, it's possible to define a disconnection
pipeline if needed.

For example, this can be useful on sites where a user that disconnects all the
related social account is required to fill a password to ensure the
authentication process in the future. This can be accomplished by overriding
the default disconnection pipeline and setup a function that checks if the user
has a password, in case it doesn't a redirect to a fill-your-password form can
be returned and later continue the disconnection process, take into account
that disconnection ensures the POST method by default, a simple method to
ensure this, is to make your form POST to ``/disconnect/`` and set the needed
password in your pipeline function. Check *Partial Pipeline* below.

In order to override the disconnection pipeline, just define the setting::

    SOCIAL_AUTH_DISCONNECT_PIPELINE = (
        'social.pipeline.disconnect.allowed_to_disconnect',
        'social.pipeline.disconnect.get_entries',
        'social.pipeline.disconnect.revoke_tokens',
        'social.pipeline.disconnect.disconnect'
    )


Partial Pipeline
----------------

It's possible to cut the pipeline process to return to the user asking for more
data and resume the process later. To accomplish this decorate the function
that will cut the process with the ``@partial`` decorator located at
``social/pipeline/partial.py``.

The old ``social.pipeline.partial.save_status_to_session`` is now deprecated.

When it's time to resume the process just redirect the user to ``/complete/<backend>/``
or ``/disconnect/<backend>/`` view. The pipeline will resume in the same
function that cut the process.

``@partial`` and ``save_status_to_session`` stores needed data into user session
under the key ``partial_pipeline``. To get the backend in order to redirect to
any social view, just do::

    backend = session['partial_pipeline']['backend']

Check the `example applications`_ to check a basic usage.


Email validation
----------------

There's a pipeline to validate email addresses, but it relies a lot on your
project.

The pipeline is at ``social.pipeline.mail.mail_validation`` and it's a partial
pipeline, it will return a redirect to an URL that you can use to tell the
users that an email validation was sent to them. If you want to mention the
email address you can get it from the session under the key ``email_validation_address``.

In order to send the validation python-social-auth_ needs a function that will
take care of it, this function is defined by the developer with the setting
``SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION``. It should be an import path. This
function should take two arguments ``strategy`` and ``code``.  ``code`` is
a model instance used to validate the email address, it contains three fields:

``code = '...'``
    Holds an ``uuid.uuid4()`` value and it's the code used to identify the
    validation process.

``email = '...'``
    Email address trying to be validate.

``verified = True / False``
    Flag marking if the email was verified or not.

You should use the code in this instance the build the link for email
validation which should go to ``/complete/email?verification_code=<code here>``, if using
Django you can do it with::

    from django.core.urlresolvers import reverse
    url = strategy.build_absolute_uri(
        reverse('social:complete', args=(strategy.backend_name,))
    ) + '?verification_code=' + code.code

On Flask::

    from flask import url_for
    url = url_for('social.complete', backend=strategy.backend_name,
                  _external=True) + '?verification_code=' + code

This pipeline can be used globally with any backend if this setting is
defined::

    SOCIAL_AUTH_FORCE_EMAIL_VALIDATION = True

Or individually by defining the setting per backend basis like
``SOCIAL_AUTH_TWITTER_FORCE_EMAIL_VALIDATION = True``.

.. _python-social-auth: https://github.com/omab/python-social-auth
.. _example applications: https://github.com/omab/python-social-auth/tree/master/examples
