Docker
======

Docker.io OAuth2
----------------

Docker.io now supports OAuth2 for their API. In order to set it up:

- Register a new application by following the instructions in their website:
  `Register Your Application`_

- Fill **Consumer Key** and **Consumer Secret** values in settings::

      SOCIAL_AUTH_DOCKER_KEY = ''
      SOCIAL_AUTH_DOCKER_SECRET = ''

- Add ``'social.backends.docker.DockerOAuth2'`` into your
  ``SOCIAL_AUTH_AUTHENTICATION_BACKENDS``.

.. _Register Your Application: http://docs.docker.io/en/latest/reference/api/docker_io_oauth_api/#register-your-application
