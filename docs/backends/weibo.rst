Weibo OAuth
===========

Weibo OAuth 2.0 workflow.

- Register a new application at Weibo_.

- Fill ``Consumer Key`` and ``Consumer Secret`` values in the settings::

      SOCIAL_AUTH_WEIBO_KEY = ''
      SOCIAL_AUTH_WEIBO_SECRET = ''

By default ``account id``, ``profile_image_url`` and ``gender`` are stored in
extra_data field.

.. _Weibo: http://open.weibo.com
