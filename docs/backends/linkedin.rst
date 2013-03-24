LinkedIn
========

LinkedIn setup is similar to any other OAuth service. The auth flow is
explained on `LinkedIn Developers`_ docs. To setup the backend follow:

- Register an app on `LinkedIn Developer Network`_

- Fill the application key and secret in your settings::

    SOCIAL_AUTH_LINKEDIN_KEY = ''
    SOCIAL_AUTH_LINKEDIN_SECRET = ''

- Application scopes can be specified by::

    SOCIAL_AUTH_LINKEDIN_SCOPE = [...]

  Check the available options at `LinkedIn Scopes`_. If you want to request
  a user's email address, you'll need specify that your application needs
  access to the email address use the ``r_emailaddress`` scope.

- To request extra fields using `LinkedIn fields selectors`_ just define this
  setting::

    SOCIAL_AUTH_LINKEDIN_FIELD_SELECTORS = [...]

  with the needed fields selectors, also define LINKEDIN_EXTRA_DATA properly as
  described in `OAuth <oauth.html>`_, that way the values will be stored in
  ``UserSocialAuth.extra_data`` field. By default ``id``, ``first-name`` and
  ``last-name`` are requested and stored.

For example, to request a user's email, headline, and industry from the
Linkedin API and store the information in ``UserSocialAuth.extra_data``, you
would add these settings::

    # Add email to requested authorizations.
    SOCIAL_AUTH_LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress', ...]
    # Add the fields so they will be requested from linkedin.
    SOCIAL_AUTH_LINKEDIN_EXTRA_FIELD_SELECTORS = ['email-address', 'headline', 'industry']
    # Arrange to add the fields to UserSocialAuth.extra_data
    SOCIAL_AUTH_LINKEDIN_EXTRA_DATA = [('id', 'id'),
                                       ('first-name', 'first_name'),
                                       ('last-name', 'last_name'),
                                       ('email-address', 'email_address'),
                                       ('headline', 'headline'),
                                       ('industry', 'industry')]

.. _LinkedIn fields selectors: http://developer.linkedin.com/docs/DOC-1014
.. _LinkedIn Scopes: https://developer.linkedin.com/documents/authentication#granting
.. _LinkedIn Developer Network: https://www.linkedin.com/secure/developer
.. _LinkedIn Developers: http://developer.linkedin.com/documents/authentication
