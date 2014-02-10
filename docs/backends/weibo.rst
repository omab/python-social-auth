Weibo OAuth
===========

Weibo OAuth 2.0 workflow.

- Register a new application at Weibo_.

- Fill ``Consumer Key`` and ``Consumer Secret`` values in the settings::

      SOCIAL_AUTH_WEIBO_KEY = ''
      SOCIAL_AUTH_WEIBO_SECRET = ''

By default ``account id``, ``profile_image_url`` and ``gender`` are stored in
extra_data field.

The user name is used by default to build the user instance ``username``,
sometimes this contains non-ASCII characters which might not be desirable for
the website. To avoid this issue it's possible to use the Weibo ``domain``
which will be inside the ASCII range by defining this setting::

    SOCIAL_AUTH_WEIBO_DOMAIN_AS_USERNAME = True

.. _Weibo: http://open.weibo.com
