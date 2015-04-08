Qiita
=====

Qiita

- Register a new application at Qiita_, set the callback URL to
  ``http://example.com/complete/qiita/`` replacing ``example.com`` with your
  domain.

- Fill ``Client ID`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_QIITA_KEY = ''
      SOCIAL_AUTH_QIITA_SECRET = ''

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_QIITA_SCOPE = [...]

  See auth scopes at `Qiita Scopes docs`_.


.. _Qiita: https://qiita.com/settings/applications
.. _Qiita Scopes docs: https://qiita.com/api/v2/docs#スコープ
