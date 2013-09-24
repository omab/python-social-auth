Google
======

This section describes how to setup the different services provided by Google.

Google OAuth
------------

Google provides ``Consumer Key`` and ``Consumer Secret`` keys to registered
applications, but also allows unregistered application to use their authorization
system with, but beware that this method will display a security banner to the
user telling that the application is not trusted.

Check `Google OAuth`_ and make your choice.

- fill ``Consumer Key`` and ``Consumer Secret`` values::

      SOCIAL_AUTH_GOOGLE_OAUTH_KEY = ''
      SOCIAL_AUTH_GOOGLE_OAUTH_SECRET = ''

anonymous values will be used if not configured as described in their
`OAuth reference`_

- setup any needed extra scope in::

      SOCIAL_AUTH_GOOGLE_OAUTH_SCOPE = [...]


Google OAuth2
-------------

Recently Google launched OAuth2 support following the definition at `OAuth2 draft`.
It works in a similar way to plain OAuth mechanism, but developers **must** register
an application and apply for a set of keys. Check `Google OAuth2`_ document for details.

**Note**:
  This support is experimental as Google implementation may change and OAuth2 is still
  a draft.

To enable OAuth2 support:

- fill ``Client ID`` and ``Client Secret`` settings, these values can be obtained
  easily as described on `OAuth2 Registering`_ doc::

      SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
      SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

- setup any needed extra scope::

      SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [...]

Check which applications can be included in their `Google Data Protocol Directory`_


Google OpenId
-------------

Google OpenId works strightforward, not settings are needed. Domains or emails
whitlists can be applied too, check `White listed domains and email addresses`_
for details.

Orkut
-----

Orkut offers per application keys named ``Consumer Key`` and ``Consumer Secret``.
To enable Orkut these two keys are needed.

Check `Google support`_ and `Orkut API`_ for details on getting keys.

- fill ``Consumer Key`` and ``Consumer Secret`` values::

      SOCIAL_AUTH_ORKUT_KEY = ''
      SOCIAL_AUTH_ORKUT_SECRET = ''

- add any needed extra data to::

      SOCIAL_AUTH_ORKUT_EXTRA_DATA = [...]

- configure extra scopes in::

      SOCIAL_AUTH_ORKUT_SCOPE = [...]


User identification
-------------------

Optional support for static and unique Google Profile ID identifiers instead of
using the e-mail address for account association can be enabled with::

      SOCIAL_AUTH_GOOGLE_OAUTH_USE_UNIQUE_USER_ID = True

or::

      SOCIAL_AUTH_GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True

depending on the backends in use.

.. _Google support: http://www.google.com/support/a/bin/answer.py?hl=en&answer=162105
.. _Orkut API:  http://code.google.com/apis/orkut/docs/rest/developers_guide_protocol.html#Authenticating
.. _Google OpenID: http://code.google.com/apis/accounts/docs/OpenID.html
.. _Google OAuth: http://code.google.com/apis/accounts/docs/OAuth.html
.. _Google OAuth2: http://code.google.com/apis/accounts/docs/OAuth2.html
.. _OAuth2 Registering: http://code.google.com/apis/accounts/docs/OAuth2.html#Registering
.. _OAuth2 draft: http://tools.ietf.org/html/draft-ietf-oauth-v2-10
.. _OAuth reference: http://code.google.com/apis/accounts/docs/OAuth_ref.html#SigningOAuth
.. _Orkut OAuth:  http://code.google.com/apis/orkut/docs/rest/developers_guide_protocol.html#Authenticating
