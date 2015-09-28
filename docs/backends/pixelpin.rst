PixelPin
========

PixelPin only supports OAuth2.

PixelPin OAuth2
---------------

Developer documentation for PixelPin can be found at http://developer.pixelpin.co.uk/
To setup OAuth2 do the following:

- Register a new developer account at `PixelPin Developers`_.

    You require a PixelPin account to create developer accounts. Sign up at `PixelPin Account Page`_
	For the value of redirect uri, use whatever path you need to return to on your web application. The
	example code provided with the plugin uses http://<yoursite>/complete/pixelpin-oauth2/
	
	Once verified by email, record the values of client id and secret for the next step

- Fill **Consumer Key** and **Consumer Secret** values in your settings.py file::

      SOCIAL_AUTH_PIXELPIN_OAUTH2_KEY = ''
      SOCIAL_AUTH_PIXELPIN_OAUTH2_SECRET = ''

- Add ``'social.backends.pixelpin.PixelPinOAuth2'`` into your
  ``SOCIAL_AUTH_AUTHENTICATION_BACKENDS``.

.. _PixelPin homepage: http://pixelpin.co.uk/
.. _PixelPin Account Page: https://login.pixelpin.co.uk/
.. _PixelPin Developers: http://developer.pixelpin.co.uk/
