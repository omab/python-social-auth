Adding a new backend
====================

Add new backends is quite easy, usually adding just a ``class`` with a couple
settings and methods overrides to retrieve user data from services API. Follow
the details below.


Common attributes
-----------------

First, lets check the common attributes for all backend types.

``name = ''``
    Any backend needs a name, usually the popular name of the service is used,
    like ``facebook``, ``twitter``, etc. It must be unique, otherwise another
    backend can take precedence if it's listed before in
    ``AUTHENTICATION_BACKENDS`` setting.

``ID_KEY = None``
    Defines the attribute in the service response that identifies the user as
    unique in the service, the value is later stored in the ``uid`` attribute
    in the ``UserSocialAuth`` instance.

``REQUIRES_EMAIL_VALIDATION = False``
    Flags the backend to enforce email validation during the pipeline (if the
    corresponding pipeline ``social.pipeline.mail.mail_validation`` was
    enabled).

``EXTRA_DATA = None``
    During the auth process some basic user data is returned by the provider or
    retrieved by ``user_data()`` method which usually is used to call some API
    on the provider to retrieve it. This data will be stored under
    ``UserSocialAuth.extra_data`` attribute, but to make it accessible under
    some common names on different providers, this attribute defines a list of
    tuples in the form ``(name, alias)`` where ``name`` is the key in the user
    data (which should be a ``dict`` instance) and ``alias`` is the name to
    store it on ``extra_data``.


OAuth
-----

OAuth1 and OAuth2 provide share some common definitions based on the shared
behavior during the auth process, like a successful API response from
``AUTHORIZATION_URL`` usually returns some basic user data like a user Id.


Shared attributes
*****************

``name``
    This defines the backend name and identifies it during the auth process.
    The name is used in the URLs ``/login/<backend name>`` and
    ``/complete/<backend name>``.

``ID_KEY = 'id'``
    Default key name where user identification field is defined, it's used on
    auth process when some basic user data is returned. This Id is stored in
    ``UserSocialAuth.uid`` field, this together the ``UserSocialAuth.provider``
    field is used to unique identify a user association.

``SCOPE_PARAMETER_NAME = 'scope'``
    Scope argument is used to tell the provider the API endpoints you want to
    call later, it's a permissions request granted over the ``access_token``
    later retrieved. Default value is ``scope`` since that's usually the name
    used in the URL parameter, but can be overridden if needed.

``DEFAULT_SCOPE = None``
    Some providers give nothing about the user but some basic data in required
    like the user Id or an email address. Default scope attribute is used to
    specify a default value for ``scope`` argument to request those extra used
    bits.

``SCOPE_SEPARATOR = ' '``
    The ``scope`` argument is usually a list of permissions to request, the
    list is joined used a separator, usually just a blank space, but differ
    from provider to provider, override the default value with this attribute
    if it differs.


OAuth2
******

OAuth2 backends are fair simple to implement, just a few settings, a method
override and it's mostly ready to go.

The key points on this backends are:

``AUTHORIZATION_URL``
    This is the entry point for the authorization mechanism, users must be
    redirected to this URL, used on ``auth_url`` method which builds the
    redirect address with ``AUTHORIZATION_URL`` plus some arguments
    (``client_id``, ``redirect_uri``, ``response_type``, and ``state``).

``ACCESS_TOKEN_URL``
    Must point to the API endpoint that provides an ``access_token`` needed to
    authenticate in users behalf on futer API calls.

``REFRESH_TOKEN_URL``
    Some providers give the option to renew the ``access_token`` since they are
    usually limited in time, once that time runs out, the token is invalidated
    and cannot be used any more. This attribute should point to that API
    endpoint.

``RESPONSE_TYPE``
    The response type expected on the auth process, default value is ``code``
    as dictated by OAuth2 definition. Override it if default value doesn't fit
    the provider implementation.

``STATE_PARAMETER``
    OAuth2 defines that an ``state`` parameter can be passed in order to
    validate the process, it's kinda a CSRF check to avoid man in the middle
    attacks. Some don't recognice it or don't return it which will making the
    auth process invalid, set this attribute as ``False`` in such case.

``REDIRECT_STATE``
    For those providers that don't recognice the ``state`` parameter, the app
    can add a ``redirect_state`` argument to the ``redirect_uri`` to mimic it.
    Set this value to ``False`` if the provider likes to verify the
    ``redirect_uri`` value and this parameter invalidates that check.


Example code::

    from social.backends.oauth import BaseOAuth2

    class GithubOAuth2(BaseOAuth2):
        """Github OAuth authentication backend"""
        name = 'github'
        AUTHORIZATION_URL = 'https://github.com/login/oauth/authorize'
        ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
        SCOPE_SEPARATOR = ','
        EXTRA_DATA = [
            ('id', 'id'),
            ('expires', 'expires')
        ]

        def get_user_details(self, response):
            """Return user details from Github account"""
            return {'username': response.get('login'),
                    'email': response.get('email') or '',
                    'first_name': response.get('name')}

        def user_data(self, access_token, *args, **kwargs):
            """Loads user data from service"""
            url = 'https://api.github.com/user?' + urlencode({
                'access_token': access_token
            })
            try:
                return json.load(self.urlopen(url))
            except ValueError:
                return None


OAuth1
******

OAuth1 process is a bit more trickier, `Twitter Docs`_ explains it quite well.
Beside the ``AUTHORIZATION_URL`` and ``ACCESS_TOKEN_URL`` attributes, a third
one is needed used when starting the process.

``REQUEST_TOKEN_URL = ''``
    During the auth process an unauthorized token is needed to start the
    process, later this token is exchanged for an ``access_token``. This
    setting points to the API endpoint where that unauthorized token can be
    retrieved.

Example code::

    from xml.dom import minidom

    from social.backends.oauth import ConsumerBasedOAuth


    class TripItOAuth(ConsumerBasedOAuth):
        """TripIt OAuth authentication backend"""
        name = 'tripit'
        AUTHORIZATION_URL = 'https://www.tripit.com/oauth/authorize'
        REQUEST_TOKEN_URL = 'https://api.tripit.com/oauth/request_token'
        ACCESS_TOKEN_URL = 'https://api.tripit.com/oauth/access_token'
        EXTRA_DATA = [('screen_name', 'screen_name')]

        def get_user_details(self, response):
            """Return user details from TripIt account"""
            try:
                first_name, last_name = response['name'].split(' ', 1)
            except ValueError:
                first_name = response['name']
                last_name = ''
            return {'username': response['screen_name'],
                    'email': response['email'],
                    'fullname': response['name'],
                    'first_name': first_name,
                    'last_name': last_name}

        def user_data(self, access_token, *args, **kwargs):
            """Return user data provided"""
            url = 'https://api.tripit.com/v1/get/profile'
            request = self.oauth_request(access_token, url)
            content = self.fetch_response(request)
            try:
                dom = minidom.parseString(content)
            except ValueError:
                return None

            return {
                'id': dom.getElementsByTagName('Profile')[0].getAttribute('ref'),
                'name': dom.getElementsByTagName(
                    'public_display_name')[0].childNodes[0].data,
                'screen_name': dom.getElementsByTagName(
                    'screen_name')[0].childNodes[0].data,
                'email': dom.getElementsByTagName(
                    'is_primary')[0].parentNode.getElementsByTagName(
                    'address')[0].childNodes[0].data,
            }


OpenId
------

OpenId is fair simpler that OAuth since it's used for authentication rather
than authorization (regardless it's used for authorization too).

A single attribute is usually needed, the authentication URL endpoint.

``URL = ''``
    OpenId endpoint where to redirect the user.

Sometimes the URL is user dependant, like in myOpenId_ where the URL is
``https://<user handler>.myopenid.com``. For those cases where the user must
input it's handle (or full URL). The backend must override the ``openid_url()``
method to retrieve it and return a full URL to where the user will be
redirected.

Example code::

    from social.backends.open_id import OpenIdAuth
    from social.exceptions import AuthMissingParameter


    class LiveJournalOpenId(OpenIdAuth):
        """LiveJournal OpenID authentication backend"""
        name = 'livejournal'

        def get_user_details(self, response):
            """Generate username from identity url"""
            values = super(LiveJournalOpenId, self).get_user_details(response)
            values['username'] = values.get('username') or \
                                 urlparse.urlsplit(response.identity_url)\
                                            .netloc.split('.', 1)[0]
            return values

        def openid_url(self):
            """Returns LiveJournal authentication URL"""
            if not self.data.get('openid_lj_user'):
                raise AuthMissingParameter(self, 'openid_lj_user')
            return 'http://%s.livejournal.com' % self.data['openid_lj_user']


Auth APIs
---------

For others authentication types, a ``BaseAuth`` class is defined to help. Those
custom auth methods must override the ``auth_url()`` and ``auth_complete()``
methods.

Example code::

    from google.appengine.api import users

    from social.backends.base import BaseAuth
    from social.exceptions import AuthException


    class GoogleAppEngineAuth(BaseAuth):
        """GoogleAppengine authentication backend"""
        name = 'google-appengine'

        def get_user_id(self, details, response):
            """Return current user id."""
            user = users.get_current_user()
            if user:
                return user.user_id()

        def get_user_details(self, response):
            """Return user basic information (id and email only)."""
            user = users.get_current_user()
            return {'username': user.user_id(),
                    'email': user.email(),
                    'fullname': '',
                    'first_name': '',
                    'last_name': ''}

        def auth_url(self):
            """Build and return complete URL."""
            return users.create_login_url(self.redirect_uri)

        def auth_complete(self, *args, **kwargs):
            """Completes login process, must return user instance."""
            if not users.get_current_user():
                raise AuthException('Authentication error')
            kwargs.update({'response': '', 'backend': self})
            return self.strategy.authenticate(*args, **kwargs)


.. _Twitter Docs: https://dev.twitter.com/docs/auth/implementing-sign-twitter
.. _myOpenId: https://www.myopenid.com/
