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


.. _python-social-auth: https://github.com/omab/python-social-auth
