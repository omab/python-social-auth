GitHub
======

GitHub works similar to Facebook (OAuth).

- Register a new application at `GitHub Developers`_, set the callback URL to
  ``http://example.com/complete/github/`` replacing ``example.com`` with your
  domain.

- Fill the ``Client ID`` and ``Client Secret`` values from GitHub in the settings::

      SOCIAL_AUTH_GITHUB_KEY = ''
      SOCIAL_AUTH_GITHUB_SECRET = ''

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_GITHUB_SCOPE = [...]


GitHub for Organizations
------------------------

When defining authentication for organizations, use the
``GithubOrganizationOAuth2`` backend instead. The settings are the same as
the non-organization backend, but the names must be::

      SOCIAL_AUTH_GITHUB_ORG_*

Be sure to define the organization name using the setting::

      SOCIAL_AUTH_GITHUB_ORG_NAME = ''

This name will be used to check that the user really belongs to the given
organization and discard it if they're not part of it.


GitHub for Teams
----------------

Similar to ``GitHub for Organizations``, there's a GitHub for Teams backend,
use the backend ``GithubTeamOAuth2``. The settings are the same as
the basic backend, but the names must be::

    SOCIAL_AUTH_GITHUB_TEAM_*

Be sure to define the ``Team ID`` using the setting::

      SOCIAL_AUTH_GITHUB_TEAM_ID = ''

This ``id`` will be used to check that the user really belongs to the given
team and discard it if they're not part of it.


Github for Enterprises
----------------------

Check the docs :ref:`github-enterprise` if planning to use Github
Enterprises.


.. _GitHub Developers: https://github.com/settings/applications/new
