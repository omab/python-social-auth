Steam OpenId
============

Steam OpenId works quite straightforward, but to retrieve some user data (known
as ``player`` on Steam API) a Steam API Key is needed.

Configurable settings:

- Supply a Steam API Key from `Steam Dev`_::

    SOCIAL_AUTH_STEAM_API_KEY = key


- To save ``player`` data provided by Steam into ``extra_data``::

    SOCIAL_AUTH_STEAM_EXTRA_DATA = ['player']


.. _Steam Dev: http://steamcommunity.com/dev/apikey
