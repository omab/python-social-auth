Amazon
======

Amazon implemented OAuth2 protocol for their authentication mechanism. To
enable ``python-social-auth`` support follow this steps:

1. Go to `Amazon App Console`_ and create an application.

2. Fill App Id and Secret in your project settings::

    SOCIAL_AUTH_AMAZON_KEY = '...'
    SOCIAL_AUTH_AMAZON_SECRET = '...'

3. Enable the backend::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.amazon.AmazonOAuth2',
        ...
    )

Further documentation at `Website Developer Guide`_ and `Getting Started for Web`_.

**Note:** This backend supports TLSv1 protocol since SSL will be deprecated
          from May 25, 2015

.. _Amazon App Console: http://login.amazon.com/manageApps
.. _Website Developer Guide: https://images-na.ssl-images-amazon.com/images/G/01/lwa/dev/docs/website-developer-guide._TTH_.pdf
.. _Getting Started for Web: http://login.amazon.com/website
