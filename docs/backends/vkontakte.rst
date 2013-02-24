VKontakte
=========

VKontakte auth service support.

OAuth2
------

VKontakte uses OAuth2 for Authentication.

- Register a new application at the `Vkontakte API`_,

- fill ``Application Id`` and ``Application Secret`` values in the settings::

      SOCIAL_AUTH_VKONTAKTE_OAUTH2_KEY = ''
      SOCIAL_AUTH_VKONTAKTE_OAUTH2_SECRET = ''

- Add ``'social.backends.vkontakte.VKontakteOAuth2'`` into your ``AUTHENTICATION_BACKENDS``.

- Then you can start using ``/login/vkontakte-oauth2`` in your link href.

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_VKONTAKTE_OAUTH2_SCOPE = [...]

  See the `names of the privileges VKontakte`_.


OAuth2 Application
------------------

To support OAuth2 authentication for VKontakte applications:

- Fill ``Application ID`` and ``Application Secret`` settings::

    SOCIAL_AUTH_VKONTAKTE_APP_ID = ''
    SOCIAL_AUTH_VKONTAKTE_APP_SECRET = ''

- Fill ``user_mode``::

    SOCIAL_AUTH_VKONTAKTE_APP_USER_MODE = 2

  Possible values:
    - ``0``: there will be no check whether a user connected to your
      application or not
    - ``1``: ``python-social-auth`` will check ``is_app_user`` parameter
      VKontakte sends when user opens application page one time
    - ``2``: (safest) ``python-social-auth`` will check status of user
      interactively (useful when you have interactive authentication via AJAX)

- Create your IFrame application at VKontakte.

- In application settings specify your IFrame URL ``mysite.com/vk`` (current
  default).

- Add a snippet similar to this into your login template::

    <script src="http://vkontakte.ru/js/api/xd_connection.js?2" type="text/javascript"></script>
    <script type="text/javascript">
        VK.init(function() {
                VK.addCallback("onApplicationAdded", requestRights);
                VK.addCallback("onSettingsChanged", onSettingsChanged);
            }
        );

        function startConnect() {
            VK.callMethod('showInstallBox');
        }

        function requestRights() {
            VK.callMethod('showSettingsBox', 1 + 2); // 1+2 is just an example
        }

        function onSettingsChanged(settings) {
            window.location.reload();
        }
    </script>
    <a href="#" onclick="startConnect(); return false;">Click to authenticate</a>

To test, launch the server using ``sudo ./manage.py mysite.com:80`` for
browser to be able to load it when VKontakte calls IFrame URL. Open your
VKontakte application page via http://vk.com/app<app_id>. Now you are able to
connect to application and login automatically after connection when visiting
application page.

For more details see `authentication for VKontakte applications`_


OpenAPI
-------

You can also use VKontakte's own OpenAPI to log in, but you need to provide
HTML template with JavaScript code to authenticate, check below for an example.

- Get an OpenAPI App Id and add it to the settings::

    SOCIAL_AUTH_VKONTAKTE_APP_ID = ''

  This app id will be passed to the template as ``VK_APP_ID``.

Snippet example::

    <script src="http://vkontakte.ru/js/api/openapi.js" type="text/javascript"></script>
    <script type="text/javascript">
        var vkAppId = {{ VK_APP_ID|default:"null" }};
        if (vkAppId) {
            VK.init({ apiId: vkAppId });
        }
        function authVK () {
            if (!vkAppId) {
                alert ("Please specify VKontakte APP ID in your local settings file");
                return false;
            }
            VK.Auth.login(function(response) {
                var params = "";
                if (response.session) {
                    params = "first_name=" + encodeURI(response.session.user.first_name) + "&last_name=" + encodeURI(response.session.user.last_name);
                    params += "&nickname=" + encodeURI(response.session.user.nickname) + "&id=" + encodeURI(response.session.user.id);
                }
                window.location = "{{ VK_COMPLETE_URL }}?" + params;
            });
            return false;
        }
    </script>
    <a href="javascript:void(0);" onclick="authVK();">Click to authorize</a>


.. _Vkontakte OAuth: http://vk.com/developers.php?oid=-1&p=%D0%90%D0%B2%D1%82%D0%BE%D1%80%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F_%D1%81%D0%B0%D0%B9%D1%82%D0%BE%D0%B2
.. _names of the privileges VKontakte: http://vk.com/developers.php?oid=-1&p=%D0%9F%D1%80%D0%B0%D0%B2%D0%B0_%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0_%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B9
.. _Vkontakte API: http://vk.com/developers.php
.. _authentication for VKontakte applications: http://www.ikrvss.ru/2011/11/08/django-social-auh-and-vkontakte-application/
