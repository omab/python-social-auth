GitHub
======

Github works similar to Facebook (OAuth).

- Register a new application at `GitHub Developers`_, set the callback URL to
  ``http://example.com/complete/github/`` replacing ``example.com`` with your
  domain.

- Fill ``App Id`` and ``App Secret`` values in the settings::

      SOCIAL_AUTH_GITHUB_KEY = ''
      SOCIAL_AUTH_GITHUB_SECRET = ''

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_GITHUB_SCOPE = [...]


Github for Organizations
------------------------

When defining authentication for organizations, use the
``GithubOrganizationOAuth2`` backend instead. The settings are the same than
the non-organization backend, but the names must be::

    SOCIAL_AUTH_GITHUB_ORG_*

Be sure to define the organization name using the setting::

      SOCIAL_AUTH_GITHUB_ORG_NAME = ''

This name will be used to check that the user really belongs to the given
organization and discard it in case he's not part of it.

.. _GitHub Developers: https://github.com/settings/applications/new
