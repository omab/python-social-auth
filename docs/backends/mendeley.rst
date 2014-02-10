Mendeley
========

Mendeley supports OAuth1 and OAuth2, they are in the process of deprecating
OAuth1 API (which should be fully deprecated on April 2014, check their
announcement_).


OAuth1
------

In order to support OAuth1 (not recomended, use OAuth2 instead):

- Register a new application at `Mendeley Application Registration`_

- Fill **Consumer Key** and **Consumer Secret** values::

      SOCIAL_AUTH_MENDELEY_KEY = ''
      SOCIAL_AUTH_MENDELEY_SECRET = ''


OAuth2
------

In order to support OAuth2:

- Register a new application at `Mendeley Application Registration`_, or
  migrate your OAuth1 application, check their `migration steps here`_.

- Fill **Application ID** and **Application Secret** values::

      SOCIAL_AUTH_MENDELEY_OAUTH2_KEY = ''
      SOCIAL_AUTH_MENDELEY_OAUTH2_SECRET = ''


.. _Mendeley Application Registration: http://dev.mendeley.com/applications/register/
.. _announcement: https://sites.google.com/site/mendeleyapi/home/authentication
.. _migration steps here: https://groups.google.com/forum/#!topic/mendeley-open-api-developers/KmUQW9I0ST0
