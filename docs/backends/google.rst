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


Google+ Sign-In
---------------

`Google+ Sign In`_ works a lot like OAuth2, but most of the initial work is
done by their Javascript which thens calls a defined handler to complete the
auth process.

* To enable the backend create an application using the `Google console`_ and
  fill the key settings::

    SOCIAL_AUTH_GOOGLE_PLUS_KEY = '...'
    SOCIAL_AUTH_GOOGLE_PLUS_SECRET = '...'

* Add their button snippet to your template::

    <div id="signinButton">
        <span class="g-signin" data-scope="{{ plus_scope }}"
                               data-clientid="{{ plus_id }}"
                               data-redirecturi="postmessage"
                               data-accesstype="offline"
                               data-cookiepolicy="single_host_origin"
                               data-callback="signInCallback">
        </span>
    </div>

  ``signInCallback`` is the name of your Javascript callback function.

* The scope can be generated doing::

    from social.backends.google import GooglePlusAuth
    plus_scope = ' '.join(GooglePlusAuth.DEFAULT_SCOPE)

  Or get the value from settings if it was overridden. ``plus_id`` is the value
  from ``SOCIAL_AUTH_GOOGLE_PLUS_KEY``.

* Add the Javascript snippet::

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js" type="text/javascript"></script>
    <script type="text/javascript">
        (function () {
            var po = document.createElement('script');
            po.type = 'text/javascript';
            po.async = true;
            po.src = 'https://plus.google.com/js/client:plusone.js?onload=start';
            var s = document.getElementsByTagName('script')[0];
            s.parentNode.insertBefore(po, s);
        })();
    </script>

* Define your Javascript callback function::

    <script type="text/javascript">
        var signInCallback = function (result) {
            if (result['error']) {
                alert('An error happened:', result['error']);
            } else {
                $('#code').attr('value', result['code']);
                $('#at').attr('value', result['access_token']);
                $('#google-plus').submit();
            }
        };
    </script>

  In the example above the values needed to complete the auth process are
  posted using a form like this but this is just a simple example::

    <form id="google-plus" method="post" action="{% url 'social:complete' "google-plus" %}">{% csrf_token %}
        <input id="at" type="hidden" name="access_token" value="" />
        <input id="code" type="hidden" name="code" value="" />
    </form>


Google OpenId
-------------

Google OpenId works straightforward, not settings are needed. Domains or emails
whitelists can be applied too, check the whitelists_ settings for details.


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
.. _Google Data Protocol Directory: http://code.google.com/apis/gdata/docs/directory.html
.. _whitelists: ../configuration/settings.html#whitelists
.. _Google+ Sign In: https://developers.google.com/+/web/signin/
.. _Google console: https://code.google.com/apis/console
