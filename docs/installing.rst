Installation
============

Dependencies
------------

Dependencies that **must** be meet to use the application:

- OpenId_ support depends on python-openid_

- OAuth_ support depends on python-oauth2_ (despite the name, this is just for
  OAuth1)

- Several backends demands application registration on their corresponding
  sites and other dependencies like sqlalchemy_ on Flask and Webpy.


Get a copy
----------

From pypi_::

    $ pip install python-social-auth

Or::

    $ easy_install python-social-auth

Or clone from github_::

    $ git clone git://github.com/omab/python-social-auth.git

And add social to ``PYTHONPATH``::

    $ export PYTHONPATH=$PYTHONPATH:$(pwd)/python-social-auth/

Or::

    $ cd python-social-auth
    $ sudo python setup.py install


.. _OpenId: http://openid.net/
.. _OAuth: http://oauth.net/
.. _pypi: http://pypi.python.org/pypi/python-social-auth/
.. _github: https://github.com/omab/python-social-auth
.. _python-openid: http://pypi.python.org/pypi/python-openid/
.. _python-oauth2: https://github.com/simplegeo/python-oauth2
.. _sqlalchemy: http://www.sqlalchemy.org/
