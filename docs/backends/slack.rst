Slack
=====

Slack

- Register a new application at `https://api.slack.com/applications`_, set the
  callback URL to ``http://example.com/complete/slack/`` replacing
  ``example.com`` with your domain.

- Fill ``Client ID`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_SLACK_KEY = ''
      SOCIAL_AUTH_SLACK_SECRET = ''

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_SLACK_SCOPE = [...]

  See auth scopes at https://api.slack.com/docs/oauth
