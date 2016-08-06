Battle.net
==========

Blizzard implemented OAuth2 protocol for their authentication mechanism. To
enable ``python-social-auth`` support follow this steps:

1. Go to `Battlenet Developer Portal`_ and create an application.

2. Fill App Id and Secret in your project settings::

	SOCIAL_AUTH_BATTLENET_OAUTH2_KEY = '...'
	SOCIAL_AUTH_BATTLENET_OAUTH2_SECRET = '...'

3. Enable the backend::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.battlenet.BattleNetOAuth2',
        ...
    )

Note: If you want to allow the user to choose a username from his own
characters, some further steps are required, see the use cases part of the
documentation. To get the account id and battletag use the user_data function, as
`account id is no longer passed inherently`_.

Another note: If you get a 500 response "Internal Server Error" the API now requires `https on callback endpoints`_.

Further documentation at `Developer Guide`_.

.. _Battlenet Developer Portal: https://dev.battle.net/
.. _Developer Guide: https://dev.battle.net/docs/read/oauth
.. _https on callback endpoints: http://us.battle.net/en/forum/topic/17085510584
.. _account id is no longer passed inherently: http://us.battle.net/en/forum/topic/18300183303
