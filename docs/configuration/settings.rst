Configuration
=============

Application setup
-----------------

Once the application was installed (check Installation_) define the following
settings to enable the application behavior. Also check the sections dedicated
to each framework for detailed instructions.


Settings name
-------------

Almost all settings are prefixed with ``SOCIAL_AUTH_``, there are some
exceptions for Django framework like ``AUTHENTICATION_BACKENDS``.

All settings can be defined per-backend by adding the backend name to the
setting name like ``SOCIAL_AUTH_TWITTER_LOGIN_URL``. Settings discovery is done
by reducing the name starting with backend setting, then app setting and
finally global setting, for example::

    SOCIAL_AUTH_TWITTER_LOGIN_URL
    SOCIAL_AUTH_LOGIN_URL
    LOGIN_URL

The backend name is generated from the ``name`` attribute from the backend
class by uppercasing it and replacing ``-`` with ``_``.


Keys and secrets
----------------

- Setup needed OAuth keys (see OAuth_ section for details)::

    SOCIAL_AUTH_TWITTER_KEY = 'foobar'
    SOCIAL_AUTH_TWITTER_SECRET = 'bazqux'

OpenId backends don't require keys usually, but some need some API Key to
call any API on the provider. Check Backends_ sections for details.


Authentication backends
-----------------------

Register the backends you plan to use, on Django framework use the usual
``AUTHENTICATION_BACKENDS`` settings, for others, define
``SOCIAL_AUTH_AUTHENTICATION_BACKENDS``::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        'social.backends.open_id.OpenIdAuth',
        'social.backends.google.GoogleOpenId',
        'social.backends.google.GoogleOAuth2',
        'social.backends.google.GoogleOAuth',
        'social.backends.twitter.TwitterOAuth',
        'social.backends.yahoo.YahooOpenId',
        ...
    )


URLs options
------------

These URLs are used on different steps of the auth process, some for successful
results and others for error situations.

``SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/logged-in/'``
    Used to redirect the user once the auth process ended successfully. The
    value of ``?next=/foo`` is used if it was present

``SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'``
    URL where the user will be redirected in case of an error

``SOCIAL_AUTH_LOGIN_URL = '/login-url/'``
    Is used as a fallback for ``LOGIN_ERROR_URL``

``SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/new-users-redirect-url/'``
    Used to redirect new registered users, will be used in place of
    ``SOCIAL_AUTH_LOGIN_REDIRECT_URL`` if defined.

``SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/new-association-redirect-url/'``
    Like ``SOCIAL_AUTH_NEW_USER_REDIRECT_URL`` but for new associated accounts
    (user is already logged in). Used in place of ``SOCIAL_AUTH_LOGIN_REDIRECT_URL``

``SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account-disconnected-redirect-url/'``
    The user will be redirected to this URL when a social account is
    disconnected

``SOCIAL_AUTH_INACTIVE_USER_URL = '/inactive-user/'``
    Inactive users can be redirected to this URL when trying to authenticate.

Successful URLs will default to ``SOCIAL_AUTH_LOGIN_URL`` while error URLs will
fallback to ``SOCIAL_AUTH_LOGIN_ERROR_URL``.


User model
----------

``UserSocialAuth`` instances keep a reference to the ``User`` model of your
project, since this is not know, the ``User`` model must be configured by
a setting::

    SOCIAL_AUTH_USER_MODEL = 'foo.bar.User'

``User`` model must have a ``username`` and ``email`` field, these are
required.

Also an ``is_authenticated`` and ``is_active`` boolean flags are recommended,
these can be methods if necessary (must return ``True`` or ``False``). If the
model lacks them a ``True`` value is assumed.


Tweaking some fields length
---------------------------

Some databases impose limitations to indexes columns (like MySQL InnoDB), these
limitations won't play nice on some ``UserSocialAuth`` fields. To avoid such
error define some of the following settings.

``SOCIAL_AUTH_UID_LENGTH = <int>``
    Used to define the max length of the field `uid`. A value of 223 should work
    when using MySQL InnoDB which impose a 767 bytes limit (assuming UTF-8
    encoding).

``SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = <int>``
    ``Nonce`` model has a unique constraint over ``('server_url', 'timestamp',
    'salt')``, salt has a max length of 40, so ``server_url`` length must be
    tweaked using this setting.

``SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = <int>`` or ``SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = <int>``
    ``Association`` model has a unique constraint over ``('server_url',
    'handle')``, both fields lengths can be tweaked by these settings.


Username generation
-------------------

Some providers return an username, others just an Id or email or first and last
names. The application tries to build a meaningful username when possible but
defaults to generating one if needed.

An UUID is appended to usernames in case of collisions. Here are some settings
to control usernames generation.

``SOCIAL_AUTH_DEFAULT_USERNAME = 'foobar'``
    Default value to use as username, can be a callable. An UUID will be
    appended in case of duplicate entries.
    
``SOCIAL_AUTH_UUID_LENGTH = 16``
    This controls the length of the UUID appended to usernames.

``SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True``
    If you want to use the full email address as the ``username``, define this
    setting.

``SOCIAL_AUTH_SLUGIFY_USERNAMES = False``
    For those that prefer slugged usernames, the ``get_username`` pipeline can
    apply a slug transformation (code borrowed from Django project) by defining
    this setting to ``True``. The feature is disabled by default to to not
    force this option to all projects.

``SOCIAL_AUTH_CLEAN_USERNAMES = True``
    By default the regex ``r'[^\w.@+-_]+'`` is applied over usernames to clean
    them from usual undesired characters like spaces. Set this setting to
    ``False`` to disable this behavior.


Extra arguments on auth processes
---------------------------------

Some providers accept particular GET parameters that produce different results
during the auth process, usually used to show different dialog types (mobile
version, etc).

You can send extra parameters on auth process by defining settings per backend,
example to request Facebook to show Mobile authorization page, define::

      FACEBOOK_AUTH_EXTRA_ARGUMENTS = {'display': 'touch'}

For other providers, just define settings in the form::

      <uppercase backend name>_AUTH_EXTRA_ARGUMENTS = {...}

Also, you can send extra parameters on request token process by defining
settings in the same way explained above but with this other suffix::

      <uppercase backend name>_REQUEST_TOKEN_EXTRA_ARGUMENTS = {...}


Processing redirects and urlopen
--------------------------------

The application issues several redirects and API calls, this following settings
allow some tweaks to the behavior of these.

``SOCIAL_AUTH_SANITIZE_REDIRECTS = False``
    The auth process finishes with a redirect, by default it's done to the
    value of ``SOCIAL_AUTH_LOGIN_REDIRECT_URL`` but can be overridden with
    ``next`` GET argument. If this settings is ``True``, this application will
    very the domain of the final URL and only redirect to it if it's on the
    same domain.
   
``SOCIAL_AUTH_REDIRECT_IS_HTTPS = False``
    On projects behind a reverse proxy that uses HTTPS, the redirect URIs
    can became with the wrong schema (``http://`` instead of ``https://``) when
    the request lacks some headers, and might cause errors with the auth
    process, to force HTTPS in the final URIs set this setting to ``True``

``SOCIAL_AUTH_URLOPEN_TIMEOUT = 30``
    Any ``urllib2.urlopen`` call will be performed with the default timeout
    value, to change it without affecting the global socket timeout define this
    setting (the value specifies timeout seconds).

    ``urllib2.urlopen`` uses ``socket.getdefaulttimeout()`` value by default, so
    setting ``socket.setdefaulttimeout(...)`` will affect ``urlopen`` when this
    setting is not defined, otherwise this setting takes precedence. Also this
    might affect other places in Django.

    ``timeout`` argument was introduced in python 2.6 according to `urllib2
    documentation`_


Whitelists
----------

Registration can be limited to a set of users identified by their email
address or domain name. To white-list just set any of these settings:

``SOCIAL_AUTH_<BACKEND_NAME>_WHITELISTED_DOMAINS = ['foo.com', 'bar.com']``
    Supply a list of domain names to be white-listed. Any user with an email
    address on any of the allowed domains will login successfully, otherwise
    ``AuthForbidden`` is raised.

``SOCIAL_AUTH_<BACKEND_NAME>_WHITELISTED_EMAILS = ['me@foo.com', 'you@bar.com']``
    Supply a list of email addresses to be white-listed. Any user with an email
    address in this list will login successfully, otherwise ``AuthForbidden``
    is raised.


Miscellaneous settings
----------------------

``SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email',]``
    The `user_details` pipeline processor will set certain fields on user
    objects, such as ``email``. Set this to a list of fields you only want to
    set for newly created users and avoid updating on further logins.

``SOCIAL_AUTH_SESSION_EXPIRATION = True``
    Some providers return the time that the access token will live, the value is
    stored in ``UserSocialAuth.extra_data`` under the key ``expires``. By default
    the current user session is set to expire if this value is present, this
    behavior can be disabled by setting.

``SOCIAL_AUTH_OPENID_PAPE_MAX_AUTH_AGE = <int value>``
    Enable `OpenID PAPE`_ extension support by defining this setting.

``SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['foo',]``
    If you want to store extra parameters from POST or GET in session, like it
    was made for ``next`` parameter, define this setting with the parameter
    names.

    In this case ``foo`` field's value will be stored when user follows this
    link ``<a href="{% url socialauth_begin 'github' %}?foo=bar">...</a>``.


Account disconnection
---------------------

Disconnect is an side-effect operation and should be done by POST method only,
some CSRF protection is encouraged (and enforced on Django app). Ensure that
any call to `/disconnect/<backend>/` or `/disconnect/<backend>/<id>/` is done
using POST.


.. _urllib2 documentation: http://docs.python.org/library/urllib2.html#urllib2.urlopen
.. _OpenID PAPE: http://openid.net/specs/openid-provider-authentication-policy-extension-1_0.html
.. _Installation: ../installing.html
.. _Backends: ../backends/index.html
.. _OAuth: http://oauth.net/
