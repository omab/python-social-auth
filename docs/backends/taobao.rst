Taobao OAuth
============

Taobao OAuth 2.0 workflow.

- Register a new application at Open `Open Taobao`_.

- Fill ``Consumer Key`` and ``Consumer Secret`` values in the settings::

      SOCIAL_AUTH_TAOBAO_KEY = ''
      SOCIAL_AUTH_TAOBAO_SECRET = ''

By default ``token`` is stored in ``extra_data`` field.

.. _Open Taobao: http://open.taobao.com
