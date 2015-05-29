DigitalOcean
============

DigitalOcean uses OAuth2 for its auth process. See the full `DigitalOcean
developer's documentation`_ for more information.

- Register a new application in the `Apps & API page`_ in the DigitalOcean
  control panel, setting the callback URL to ``http://example.com/complete/digitalocean/``
  replacing ``example.com`` with your domain.

- Fill the ``Client ID`` and ``Client Secret`` values from GitHub in the settings::

      SOCIAL_AUTH_DIGITALOCEAN_KEY = ''
      SOCIAL_AUTH_DIGITALOCEAN_SECRET = ''

- By default, only ``read`` permissions are granted. In order to create,
  destroy, and take other actions on the user's resources, you must request
  ``read write`` permissions like so::

      SOCIAL_AUTH_DIGITALOCEAN_AUTH_EXTRA_ARGUMENTS = {'scope': 'read write'}


.. _DigitalOcean developer's documentation: https://developers.digitalocean.com/documentation/
.. _Apps & API page: https://cloud.digitalocean.com/settings/applications
