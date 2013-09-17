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
be returned and later continue the disconnection process. Check *Partial
Pipeline* below.

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

.. _python-social-auth: https://github.com/omab/python-social-auth
.. _example applications: https://github.com/omab/python-social-auth/tree/master/examples
