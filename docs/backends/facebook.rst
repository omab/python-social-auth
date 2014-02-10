Facebook
========

OAuth2
------

Facebook uses OAuth2 for its auth process. Further documentation at `Facebook
development resources`_:

- Register a new application at `Facebook App Creation`_, and

- fill ``App Id`` and ``App Secret`` values in values::

      SOCIAL_AUTH_FACEBOOK_KEY = ''
      SOCIAL_AUTH_FACEBOOK_SECRET = ''

- Define ``SOCIAL_AUTH_FACEBOOK_SCOPE`` to get extra permissions
  from facebook. Email is not sent by deafault, to get it, you must request the
  ``email`` permission::

     SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

- Define ``SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS`` to pass extra parameters
  to https://graph.facebook.com/me when gathering the user profile data, like::

    SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'ru_RU'}

If you define a redirect URL in Facebook setup page, be sure to not define
http://127.0.0.1:8000 or http://localhost:8000 because it won't work when
testing. Instead I define http://myapp.com and setup a mapping on ``/etc/hosts``.


Canvas Application
------------------

If you need to perform authentication from Facebook Canvas application:

- Create your canvas application at http://developers.facebook.com/apps

- In Facebook application settings specify your canvas URL ``mysite.com/fb``
  (current default)

- Setup your Python Social Auth settings and your application namespace::

    SOCIAL_AUTH_FACEBOOK_APP_KEY = ''
    SOCIAL_AUTH_FACEBOOK_APP_SECRET = ''
    SOCIAL_AUTH_FACEBOOK_APP_NAMESPACE = ''

- Launch your testing server on port 80 (use sudo or nginx or apache) for
  browser to be able to load it when Facebook calls canvas URL

- Open your Facebook page via http://apps.facebook.com/app_namespace or
  better via http://www.facebook.com/pages/user-name/user-id?sk=app_app-id

- After that you will see this page in a right way and will able to connect
  to application and login automatically after connection

- Provide a template to be rendered, it must have this JavaScript snippet (or
  similar) in it::

    <script type="text/javascript">
        var domain = 'https://apps.facebook.com/',
            redirectURI = domain + {{ FACEBOOK_APP_NAMESPACE }} + '/';

        window.top.location = 'https://www.facebook.com/dialog/oauth/' +
                                    '?client_id={{ FACEBOOK_KEY }}' +
                                    '&redirect_uri=' + encodeURIComponent(redirectURI) +
                                    '&scope={{ FACEBOOK_EXTENDED_PERMISSIONS }}';
    </script>


More info on the topic at `Facebook Canvas Application Authentication`_.

.. _Facebook development resources: http://developers.facebook.com/docs/authentication/
.. _Facebook App Creation: http://developers.facebook.com/setup/
.. _Facebook Canvas Application Authentication: http://www.ikrvss.ru/2011/09/22/django-social-auth-and-facebook-canvas-applications/
