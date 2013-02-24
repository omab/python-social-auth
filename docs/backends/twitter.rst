Twitter
=======

Twitter offers per application keys named ``Consumer Key`` and ``Consumer Secret``.
To enable Twitter these two keys are needed. Further documentation at
`Twitter development resources`_:

- Register a new application at `Twitter App Creation`_,

- mark the **Yes, use Twitter for login** checkbox, and

- fill **Consumer Key** and **Consumer Secret** values::

      SOCIAL_AUTH_TWITTER_KEY = ''
      SOCIAL_AUTH_TWITTER_SECRET = ''

- You need to specify an URL callback or the application will be marked as
  Client type instead of the Browser. Almost any dummy value will work if
  you plan some test.

Twitter usually fails with a 401 error when trying to call the request-token
URL, this is usually caused by server datetime errors (check miscellaneous
section). Installing ``ntp`` and syncing the server date with some pool does
the trick.

.. _Twitter development resources: http://dev.twitter.com/pages/auth
.. _Twitter App Creation: http://twitter.com/apps/new
