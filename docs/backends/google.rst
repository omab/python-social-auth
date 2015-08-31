Google
======

This section describes how to setup the different services provided by Google.

Google OAuth
------------

.. attention:: **Google OAuth deprecation**
   Important: OAuth 1.0 was officially deprecated on April 20, 2012, and will be
   shut down on April 20, 2015. We encourage you to migrate to any of the other
   protocols.

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

When creating the application in the Google Console be sure to fill the
``PRODUCT NAME`` at ``API & auth -> Consent screen`` form.

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

* To enable the backend create an application using the `Google
  console`_ and following the steps from the `official guide`_. Make
  sure to enable the Google+ API in the console.

* Fill in the key settings looking inside the Google console the subsection
  ``Credentials`` inside ``API & auth``::

    AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.google.GooglePlusAuth',
    )

    SOCIAL_AUTH_GOOGLE_PLUS_KEY = '...'
    SOCIAL_AUTH_GOOGLE_PLUS_SECRET = '...'

  ``SOCIAL_AUTH_GOOGLE_PLUS_KEY`` corresponds to the variable ``CLIENT ID``.
  ``SOCIAL_AUTH_GOOGLE_PLUS_SECRET`` corresponds to the variable
  ``CLIENT SECRET``.

* Add the sign-in button to your template, you can use the SDK button
  or add your own and attacht he click handler to it (check `Google+ Identity Sign-In`_
  documentation about it)::

    <div id="google-plus-button">Google+ Sign In</div>

* Add the Javascript snippet in the same template as above::

    <script src="https://apis.google.com/js/api:client.js"></script>

    <script type="text/javascript">
      gapi.load('auth2', function () {
        var auth2;

        auth2 = gapi.auth2.init({
          client_id: "<PUT SOCIAL_AUTH_GOOGLE_PLUS_KEY HERE>",
          scope: "<PUT BACKEND SCOPE HERE>"
        });

        auth2.then(function () {
          var button = document.getElementById("google-plus-button");
          console.log("User is signed-in in Google+ platform?", auth2.isSignedIn.get() ? "Yes" : "No");

          auth2.attachClickHandler(button, {}, function (googleUser) {
            // Send access-token to backend to finish the authenticate
            // with your application

            var authResponse = googleUser.getAuthResponse();
            var $form;
            var $input;

            $form = $("<form>");
            $form.attr("action", "/complete/google-plus");
            $form.attr("method", "post");
            $input = $("<input>");
            $input.attr("name", "access_token");
            $input.attr("value", authResponse.access_token);
            $form.append($input);
            // Add csrf-token if needed
            $(document.body).append($form);
            $form.submit();
          });
        });
      });
    </script>
    {% endif %}

* Logging out

  Logging-out can be tricky when using the the platform SDK because it
  can trigger an automatic sign-in when listening to the user status
  change. With the method show above, that won't happen, but if the UI
  depends more in the SDK values than the backend, then things can get
  out of sync easilly. To prevent this, the user should be logged-out
  from Google+ platform too. This can be accomplished by doing::

    <script type="text/javascript">
      gapi.load('auth2', function () {
        var auth2;

        auth2 = gapi.auth2.init({
          client_id: "{{ plus_id }}",
          scope: "{{ plus_scope }}"
        });

        auth2.then(function () {
          if (auth2.isSignedIn.get()) {
            $('#logout').on('click', function (event) {
              event.preventDefault();
              auth2.signOut().then(function () {
                console.log("Logged out from Google+ platform");
                document.location = "/logout";
              });
            });
          }
        });
      });
    </script>


Google OpenId
-------------

Google OpenId works straightforward, not settings are needed. Domains or emails
whitelists can be applied too, check the whitelists_ settings for details.


Orkut
-----

As of September 30, 2014, Orkut has been `shut down`_.

User identification
-------------------

Optional support for static and unique Google Profile ID identifiers instead of
using the e-mail address for account association can be enabled with::

      SOCIAL_AUTH_GOOGLE_OAUTH_USE_UNIQUE_USER_ID = True

or::

      SOCIAL_AUTH_GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True

depending on the backends in use.


Refresh Tokens
--------------

To get an OAuth2 refresh token along with the access token, you must pass an extra argument: ``access_type=offline``.
To do this with Google+ sign-in::

      SOCIAL_AUTH_GOOGLE_PLUS_AUTH_EXTRA_ARGUMENTS = {
            'access_type': 'offline'
      }


Scopes deprecation
------------------

Google is deprecating the full-url scopes from `Sept 1, 2014`_ in favor of
``Google+ API`` and the recently introduced shorter scopes names. But
``python-social-auth`` already introduced the scopes change at e3525187_ which
was released at ``v0.1.24``.

But, to enable the new scopes the application requires ``Google+ API`` to be
enabled in the `Google console`_ dashboard, the change is quick and quite
simple, but if any developer desires to keep using the old scopes, it's
possible with the following settings::

    # Google OAuth2 (google-oauth2)
    SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
    SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]

    # Google+ SignIn (google-plus)
    SOCIAL_AUTH_GOOGLE_PLUS_IGNORE_DEFAULT_SCOPE = True
    SOCIAL_AUTH_GOOGLE_PLUS_SCOPE = [
        'https://www.googleapis.com/auth/plus.login',
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ]

To ease the change, the old API and scopes is still supported by the
application, the new values are the default option but if having troubles
supporting them you can default to the old values by defining this setting::

    SOCIAL_AUTH_GOOGLE_OAUTH2_USE_DEPRECATED_API = True
    SOCIAL_AUTH_GOOGLE_PLUS_USE_DEPRECATED_API = True

.. _Google support: http://www.google.com/support/a/bin/answer.py?hl=en&answer=162105
.. _Google OpenID: http://code.google.com/apis/accounts/docs/OpenID.html
.. _Google OAuth: http://code.google.com/apis/accounts/docs/OAuth.html
.. _Google OAuth2: http://code.google.com/apis/accounts/docs/OAuth2.html
.. _OAuth2 Registering: http://code.google.com/apis/accounts/docs/OAuth2.html#Registering
.. _OAuth2 draft: http://tools.ietf.org/html/draft-ietf-oauth-v2-10
.. _OAuth reference: http://code.google.com/apis/accounts/docs/OAuth_ref.html#SigningOAuth
.. _shut down: https://support.google.com/orkut/?csw=1#Authenticating
.. _Google Data Protocol Directory: http://code.google.com/apis/gdata/docs/directory.html
.. _whitelists: ../configuration/settings.html#whitelists
.. _Google+ Sign In: https://developers.google.com/+/web/signin/
.. _Google console: https://code.google.com/apis/console
.. _official guide: https://developers.google.com/+/web/signin/#step_1_create_a_client_id_and_client_secret
.. _Sept 1, 2014: https://developers.google.com/+/api/auth-migration#timetable
.. _e3525187: https://github.com/omab/python-social-auth/commit/e35251878a88954cecf8e575eca27c63164b9f67
.. _Google+ Identity Sign-In: https://developers.google.com/identity/sign-in/web/sign-in
