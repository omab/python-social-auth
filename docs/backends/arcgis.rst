ArcGIS
=====

ArcGIS uses OAuth2 for authentication.

- Register a new application at `ArcGIS Developer Center`_.


OAuth2
------------

1. Add the OAuth2 backend to your settings page::

	AUTHENTICATION_BACKENDS = (
		...
		'social.backends.arcgis.ArcGISOAuth2',
		...
    )

2. Fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_ARCGIS_KEY = ''
      SOCIAL_AUTH_ARCGIS_SECRET = ''


.. _ArcGIS Developer Center: https://developers.arcgis.com/
