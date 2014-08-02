Strava
=========

Strava uses OAuth v2 for Authentication.

- Register a new application at the `Strava API`_, and

- fill ``Client ID`` and ``Client Secret`` from strava.com values in the settings::

      SOCIAL_AUTH_STRAVA_KEY = ''
      SOCIAL_AUTH_STRAVA_SECRET = ''

- extra scopes can be defined by using::

    SOCIAL_AUTH_STRAVA_SCOPE = ['view_private']

.. _Strava API: https://www.strava.com/settings/api
