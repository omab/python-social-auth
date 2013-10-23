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


Notes
-----

At the moment (May 29, 2013), Amazon API doesn't work properly, for example
users are being redirected to URLs like::

    https://www.amazon.com:80/ap/signin?...

Which are invalid (``https`` over port 80?). The process works OK when removing
the ``:80`` from those URLs, but this renders the service very unusable at the
moment.

User data returned by Amazon doesn't follow the documented format::

    {
        Request-Id: "02GGTU7CWMNFTV3KH3J6",
        Profile: {
            Name: "Foo Bar",
            CustomerId: "amzn1.account.ABCDE1234",
            PrimaryEmail: "foo@bar.com"
        }
    }

Instead of::

    {
        "user_id": "amzn1.account.ABCDE1234",
        "email": "foo@bar.com",
        "name": "Foo Bar"
    }

Further documentation at `Website Developer Guide`_ and `Getting Started for Web`_.

.. _Amazon App Console: http://login.amazon.com/manageApps
.. _Website Developer Guide: https://images-na.ssl-images-amazon.com/images/G/01/lwa/dev/docs/website-developer-guide._TTH_.pdf
.. _Getting Started for Web: http://login.amazon.com/website
