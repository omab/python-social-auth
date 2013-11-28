LiveJournal
===========

LiveJournal provides OpenId, it doesn't require any major settings in order to
work, beside being defined on ``AUTHENTICATION_BACKENDS```::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.aol.AOLOpenId',
        ...
    )

LiveJournal OpenId is provided by URLs in the form ``http://<username>.livejournal.com``,
this application retrieves the ``username`` from the data in the current
request by checking a parameter named ``openid_lj_user`` which can be sent by
``POST`` or ``GET``.
