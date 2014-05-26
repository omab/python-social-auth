Spotify
=======

Spotify supports OAuth 2.

- Register a new application at `Spotify Web API`_, and follow the
  instructions below.
  
OAuth2
------

Add the Spotify OAuth2 backend to your settings page::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.spotify.SpotifyOAuth2',
        ...
    )

- Fill ``App Key`` and ``App Secret`` values in the settings::

      SOCIAL_AUTH_SPOTIFY_OAUTH2_KEY = ''
      SOCIAL_AUTH_SPOTIFY_OAUTH2_SECRET = ''

.. _Spotify Web API: https://developer.spotify.com/spotify-web-api
