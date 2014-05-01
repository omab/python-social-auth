LoginRadius
===========

LoginRadius uses OAuth2 for Authentication with other providers with an HTML
widget used to trigger the auth process.

- Register a new application at the `LoginRadius Website`_, and

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_LOGINRADIUS_KEY = ''
      SOCIAL_AUTH_LOGINRADIUS_SECRET = ''

- Since the auth process is triggered by LoginRadius JS script, you need to
  sever such content to the user, all you need to do that is a template with
  the following content::

    <div id="interfacecontainerdiv" class="interfacecontainerdiv"></div>
    <script src="https://hub.loginradius.com/include/js/LoginRadius.js"></script>
    <script type="text/javascript">
        var options = {};
        options.login = true;
        LoginRadius_SocialLogin.util.ready(function () {
            $ui = LoginRadius_SocialLogin.lr_login_settings;
            $ui.interfacesize = "";
            $ui.apikey = "{{ LOGINRADIUS_KEY }}";
            $ui.callback = "{{ LOGINRADIUS_REDIRECT_URL }}";
            $ui.lrinterfacecontainer = "interfacecontainerdiv";
            LoginRadius_SocialLogin.init(options);
        });
    </script>

  Put that content in a template named ``loginradius.html`` (accessible to your
  framework), or define a name with ``SOCIAL_AUTH_LOGINRADIUS_TEMPLATE`` setting,
  like::

    SOCIAL_AUTH_LOGINRADIUS_LOCAL_HTML = 'loginradius.html'

  The template context will have the current backend instance under the
  ``backend`` name, also the application key (``LOGINRADIUS_KEY``) and the
  redirect URL (``LOGINRADIUS_REDIRECT_URL``).

- Further documentation can be found at `LoginRadius API Documentation`_ and
  `LoginRadius Datapoints`_

.. _LoginRadius Website: https://loginradius.com/
.. _LoginRadius API Documentation: http://api.loginradius.com/help/
.. _LoginRadius Datapoints: http://www.loginradius.com/datapoints/
