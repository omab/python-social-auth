Slack
=====

Slack

- Register a new application at Slack_, set the callback URL to
  ``http://example.com/complete/slack/`` replacing ``example.com`` with your
  domain.

- Fill ``Client ID`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_SLACK_KEY = ''
      SOCIAL_AUTH_SLACK_SECRET = ''

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_SLACK_SCOPE = [...]

  See auth scopes at `Slack OAuth docs`_.


.. _Slack: https://api.slack.com/applications
.. _Slack OAuth docs: https://api.slack.com/docs/oauth
