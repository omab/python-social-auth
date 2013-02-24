Authentication Pipeline
=======================

The final process of the authentication workflow is handled by an operations
pipeline where custom functions can be added or default items can be removed to
provide a custom behavior. The default pipeline is a mechanism that creates
user instances and gathers basic data from providers.

The default pipeline is composed by::

    (
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
      pass this arguments:
        - current logged in user (if it's logged in, otherwise ``None``)
        - current request

Each pipeline entry can return a ``dict``, ``None``, any other type of return
value is treated as a response instance and returned directly to the client,
check `Partial Piepeline`_ for details.

If a ``dict`` is returned, any value in the set will be merged into the
``kwargs`` argument for the next pipeline entry, ``None`` is taken as if ``{}``
was returned.

The workflow will be cut if the exception ``social.exceptions.StopPipeline``
is raised at any point, but this should be done after a user and
social user instance are created.

Partial Pipeline
----------------

It's possible to cut the pipeline process to return to the user asking for more
data and resume the process later. To accomplish this, add the entry
``social.pipeline.partial.save_status_to_session`` (or a similar implementation)
to the pipeline setting before any entry that returns an response instance::

    SOCIAL_AUTH_PIPELINE = (
        ...
        social.pipeline.partial.save_status_to_session,
        app.pipeline.redirect_to_basic_user_data_form
        ...
    )

When it's time to resume the process just redirect the user to
``/complete/<backend>/`` view. By default the pipeline will be resumed in the
next entry after ``save_status_to_session``.

``save_status_to_session`` saves needed data into user session under the key
``partial_pipeline``.

Check the `example applications`_ to check a basic usage.

.. _example applications: https://github.com/omab/python-social-auth/tree/master/examples
