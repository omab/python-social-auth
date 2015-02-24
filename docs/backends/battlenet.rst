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

Note: The API returns an accountId which will be used as identifier for the
user.  If you want to allow the user to choose a username from his own
characters, some further steps are required, see the use cases part of the
documentation.

Further documentation at `Developer Guide`_.

.. _Battlenet Developer Portal: https://dev.battle.net/
.. _Developer Guide: https://dev.battle.net/docs/read/oauth
