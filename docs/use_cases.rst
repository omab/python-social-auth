Use Cases
=========

Some miscellaneous options and use cases for python-social-auth_.


Return the user to the original page
------------------------------------

There's a common scenario were it's desired to return the user back to the
original page from where it was requested to login. For that purpose, the usual
``next`` query-string argument is used, the value of this parameter will be
stored in the session and later used to redirect the user when login was
successful.

In order to use it just define it with your link, for instance, when using
Django::

    <a href="{% url 'social:begin' 'facebook' %}?next={{ request.path }}">Login with Facebook</a>


Pass custom GET/POST parameters and retrieve them on authentication
-------------------------------------------------------------------

In some cases, you might need to send data over the URL, and retrieve it while
processing the after-effect. For example, for conditionally executing code in
custom pipelines.

In such cases, add it to ``FIELDS_STORED_IN_SESSION``.

In your settings::

    FIELDS_STORED_IN_SESSION = ['key']

In template::

    <a href="{% url 'social:begin' 'facebook' %}?key={{ value }}">Login with Facebook</a>

In your custom pipeline, retrieve it using::

    strategy.session_get('key')



Retrieve Google+ Friends
------------------------

Google provides a `People API endpoint`_ to retrieve the people in your circles
on Google+. In order to access that API first we need to define the needed
scope::

    SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
        'https://www.googleapis.com/auth/plus.login'
    ]

Once we have the ``access token`` we can call the API like this::

    import requests

    user = User.objects.get(...)
    social = user.social_auth.get(provider='google-oauth2')
    response = requests.get(
        'https://www.googleapis.com/plus/v1/people/me/people/visible',
        params={'access_token': social.extra_data['access_token']}
    )
    friends = response.json()['items']


Associate users by email
------------------------

Sometimes it's desirable that social accounts are automatically associated if
the email already matches a user account.

For example, if a user signed up with his Facebook account, then logged out and
next time tries to use Google OAuth2 to login, it could be nice (if both social
sites have the same email address configured) that the user gets into his
initial account created by Facebook backend.

This scenario is possible by enabling the ``associate_by_email`` pipeline
function, like this::

    SOCIAL_AUTH_PIPELINE = (
        'social.pipeline.social_auth.social_details',
        'social.pipeline.social_auth.social_uid',
        'social.pipeline.social_auth.auth_allowed',
        'social.pipeline.social_auth.social_user',
        'social.pipeline.user.get_username',
        'social.pipeline.social_auth.associate_by_email',  # <--- enable this one
        'social.pipeline.user.create_user',
        'social.pipeline.social_auth.associate_user',
        'social.pipeline.social_auth.load_extra_data',
        'social.pipeline.user.user_details'
    )

This feature is disabled by default because it's not 100% secure to automate
this process with all the backends. Not all the providers will validate your
email account and others users could take advantage of that.

Take for instance User A registered in your site with the email
``foo@bar.com``. Then a malicious user registers into another provider that
doesn't validate his email with that same account. Finally this user will turn
to your site (which supports that provider) and sign up to it, since the email
is the same, the malicious user will take control over the User A account.


Signup by OAuth access_token
----------------------------

It's a common scenario that mobile applications will use an SDK to signup
a user withing the app, but that signup won't be reflected by
``python-socia-auth`` unless the corresponding database entries are created. In
order to do so, it's possible to create a view / route that creates those
entries by a given ``access_token``. Take the following code for instance (the
code follows Django conventions, but versions for others frameworks can be
implemented easily)::

    from django.contrib.auth import login
    from social.apps.django_app.utils import strategy

    # Define an URL entry to point to this view, call it passing the
    # access_token parameter like ?access_token=<token>. The URL entry must
    # contain the backend, like this:
    #
    #   url(r'^register-by-token/(?P<backend>[^/]+)/$',
    #       'register_by_access_token')

    @strategy('social:complete')
    def register_by_access_token(request, backend):
        # This view expects an access_token GET parameter
        token = request.GET.get('access_token')
        user = backend.do_auth(request.GET.get('access_token'))
        if user:
            login(request, user)
            return 'OK'
        else:
            return 'ERROR'

The snipped above is quite simple, it doesn't return JSON and usually this call
will be done by AJAX. It doesn't return the user information, but that's
something that can be extended and filled to suit the project where it's going
to be used.


.. _python-social-auth: https://github.com/omab/python-social-auth
.. _People API endpoint: https://developers.google.com/+/api/latest/people/list
