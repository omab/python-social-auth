GitHub
======

Github works similar to Facebook (OAuth).

- Register a new application at `GitHub Developers`_, set your site domain as
  the callback URL or it might cause some troubles when associating accounts,

- Fill ``App Id`` and ``App Secret`` values in the settings::

      SOCIAL_AUTH_GITHUB_KEY = ''
      SOCIAL_AUTH_GITHUB_SECRET = ''

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_GITHUB_EXTENDED_PERMISSIONS = [...]

- Optional ``GitHub Organization``, which if set will allow you to constrain
  authentication to a given GitHub organization::

      SOCIAL_AUTH_GITHUB_ORGANIZATION = ''

.. _GitHub Developers: https://github.com/settings/applications/new
