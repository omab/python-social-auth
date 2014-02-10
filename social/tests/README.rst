Testing python-social-auth
==========================

Testing the application is fair simple, just met the dependencies and run the
testing suite.

The testing suite uses HTTPretty_ to mock server responses, it's not a live
test against the providers API, to do it that way, a browser and a tool like
Selenium are needed, that's slow, prone to errors on some cases, and some of
the application examples must be running to perform the testing. Plus real Key
and Secret pairs, in the end it's a mess to test functionality which is the
real point.

By mocking the server responses, we can test the backends functionality (and
other areas too) easily and quick.


Installing dependencies
-----------------------

Go to the tests_ directory and install the dependencies listed in the
requirements.txt_. Then run with ``nosetests`` command.


Pending
-------

At the moment only OAuth1 and OAuth2 backends are being tested, and just
login and partial pipeline features are covered by the test. There's still
a lot to work on, like:

    * OpenId backends
    * Frameworks support
    * Failure cases (like authentication canceled, etc)
    * Extra data saving

.. _HTTPretty: https://github.com/gabrielfalcao/HTTPretty
.. _tests: https://github.com/omab/python-social-auth/tree/master/tests
.. _requirements.txt: https://github.com/omab/python-social-auth/blob/master/tests/requirements.txt
