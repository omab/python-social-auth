.. _github-enterprise:

GitHub Enterprise
=================

GitHub Enterprise works similar to regular Github, which is in turn based on Facebook (OAuth).

- Register a new application on your instance of `GitHub Enterprise Developers`_,
  set the callback URL to ``http://example.com/complete/github/`` replacing ``example.com``
  with your domain.

- Fill the ``Client ID`` and ``Client Secret`` values from GitHub in the settings::

      SOCIAL_AUTH_GITHUB_ENTERPRISE_KEY = ''
      SOCIAL_AUTH_GITHUB_ENTERPRISE_SECRET = ''

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_GITHUB_ENTERPRISE_SCOPE = [...]


GitHub Enterprise for Organizations
-----------------------------------

When defining authentication for organizations, use the
``GithubEnterpriseOrganizationOAuth2`` backend instead. The settings are the same as
the non-organization backend, but the names must be::

      SOCIAL_AUTH_GITHUB_ENTERPRISE_ORG_*

Be sure to define the organization name using the setting::

      SOCIAL_AUTH_GITHUB_ENTERPRISE_ORG_NAME = ''

This name will be used to check that the user really belongs to the given
organization and discard it if they're not part of it.


GitHub Enterprise for Teams
---------------------------

Similar to ``GitHub Enterprise for Organizations``, there's a GitHub for Teams backend,
use the backend ``GithubEnterpriseTeamOAuth2``. The settings are the same as
the basic backend, but the names must be::

    SOCIAL_AUTH_GITHUB_ENTERPRISE_TEAM_*

Be sure to define the ``Team ID`` using the setting::

      SOCIAL_AUTH_GITHUB_ENTERPRISE_TEAM_ID = ''

This ``id`` will be used to check that the user really belongs to the given
team and discard it if they're not part of it.

.. _GitHub Enterprise Developers: https://<your_github_enterprise_domain>/settings/applications/new
