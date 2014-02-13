Odnoklassniki.ru
================

There are two options with Odnoklassniki: either you use OAuth2 workflow to
authenticate odnoklassniki users at external site, or you authenticate users
within your IFrame application.

OAuth2
------

If you use OAuth2 workflow, you need to:

- register a new application with `OAuth registration form`_

- fill out some settings::

    SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_KEY = ''
    SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_SECRET = ''
    SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_PUBLIC_NAME = ''

- add ``'social.backends.odnoklassniki.OdnoklassnikiOAuth2'`` into your
  ``SOCIAL_AUTH_AUTHENTICATION_BACKENDS``.


IFrame applications
-------------------

If you want to authenticate users in your IFrame application,

- read `Rules for application developers`_

- fill out `Developers registration form`_

- get your personal sandbox

- fill out some settings::

    SOCIAL_AUTH_ODNOKLASSNIKI_APP_KEY = ''
    SOCIAL_AUTH_ODNOKLASSNIKI_APP_SECRET = ''
    SOCIAL_AUTH_ODNOKLASSNIKI_APP_PUBLIC_NAME = ''

- add ``'social.backends.odnoklassniki.OdnoklassnikiApp'`` into your
  ``SOCIAL_AUTH_AUTHENTICATION_BACKENDS``

- sign a public offer and do some bureaucracy

You may also use::

    SOCIAL_AUTH_ODNOKLASSNIKI_APP_EXTRA_USER_DATA_LIST

Defaults to empty tuple, for the list of available fields see `Documentation on user.getInfo`_

.. _OAuth registration form: http://dev.odnoklassniki.ru/wiki/pages/viewpage.action?pageId=13992188
.. _Rules for application developers: http://dev.odnoklassniki.ru/wiki/display/ok/Odnoklassniki.ru+Third+Party+Platform
.. _Developers registration form: http://dev.odnoklassniki.ru/wiki/pages/viewpage.action?pageId=5668937
.. _Documentation on user.getInfo: http://dev.odnoklassniki.ru/wiki/display/ok/REST+API+-+users.getInfo
