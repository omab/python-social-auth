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
--------------------------------------------------------------------------

In some cases, you might need to send data over the url, and retrieve it while processing the after-effect. 
For example, for conditionally executing code in custom pipelines. 

In such cases, add it to FIELDS_STORED_IN_SESSION.

In settings.py,::

    FIELDS_STORED_IN_SESSION = ['key']

In template,::

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


.. _python-social-auth: https://github.com/omab/python-social-auth
.. _People API endpoint: https://developers.google.com/+/api/latest/people/list
