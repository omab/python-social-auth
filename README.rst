Python Social Auth
==================

Python Social Auth is an easy-to-setup social authentication/registration
mechanism with support for several frameworks and auth providers.

Crafted using base code from django-social-auth, it implements a common interface
to define new authentication providers from third parties, and to bring support
for more frameworks and ORMs.

.. image:: https://travis-ci.org/omab/python-social-auth.png?branch=master
   :target: https://travis-ci.org/omab/python-social-auth

.. image:: https://badge.fury.io/py/python-social-auth.png
   :target: http://badge.fury.io/py/python-social-auth

.. image:: https://pypip.in/d/python-social-auth/badge.png
   :target: https://crate.io/packages/python-social-auth?version=latest

.. image:: https://d2weczhvl823v0.cloudfront.net/omab/python-social-auth/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

.. contents:: Table of Contents


Features
========

This application provides user registration and login using social sites
credentials. Here are some features, which is probably not a full list yet.


Supported frameworks
--------------------

Multiple frameworks are supported:

    * Django_
    * Flask_
    * Pyramid_
    * Webpy_
    * Tornado_

More frameworks can be added easily (and should be even easier in the future
once the code matures).


Auth providers
--------------

Several services are supported by simply defining backends (new ones can be easily added
or current ones extended):

    * Amazon_ OAuth2 http://login.amazon.com/website
    * Angel_ OAuth2
    * AOL_ OpenId http://www.aol.com/
    * Appsfuel_ OAuth2
    * Behance_ OAuth2
    * BelgiumEIDOpenId_ OpenId https://www.e-contract.be/
    * Bitbucket_ OAuth1
    * Box_ OAuth2
    * Clef_ OAuth2
    * Dailymotion_ OAuth2
    * Disqus_ OAuth2
    * Douban_ OAuth1 and OAuth2
    * Dropbox_ OAuth1 and OAuth2
    * Evernote_ OAuth1
    * Exacttarget OAuth2
    * Facebook_ OAuth2 and OAuth2 for Applications
    * Fedora_ OpenId http://fedoraproject.org/wiki/OpenID
    * Fitbit_ OAuth1
    * Flickr_ OAuth1
    * Foursquare_ OAuth2
    * `Google App Engine`_ Auth
    * Github_ OAuth2
    * Google_ OAuth1, OAuth2 and OpenId
    * Instagram_ OAuth2
    * Jawbone_ OAuth2 https://jawbone.com/up/developer/authentication
    * Linkedin_ OAuth1
    * Live_ OAuth2
    * Livejournal_ OpenId
    * Mailru_ OAuth2
    * Mendeley_ OAuth1 http://mendeley.com
    * Mixcloud_ OAuth2
    * `Mozilla Persona`_
    * Odnoklassniki_ OAuth2 and Application Auth
    * OpenId_
    * OpenStreetMap_ OAuth1 http://wiki.openstreetmap.org/wiki/OAuth
    * OpenSuse_ OpenId http://en.opensuse.org/openSUSE:Connect
    * Orkut_ OAuth1
    * PixelPin_ OAuth2
    * Pocket_ OAuth2
    * Podio_ OAuth2
    * Rdio_ OAuth1 and OAuth2
    * Readability_ OAuth1
    * Reddit_ OAuth2 https://github.com/reddit/reddit/wiki/OAuth2
    * Shopify_ OAuth2
    * Skyrock_ OAuth1
    * Soundcloud_ OAuth2
    * Stackoverflow_ OAuth2
    * Steam_ OpenId
    * Stocktwits_ OAuth2
    * Stripe_ OAuth2
    * Taobao_ OAuth2 http://open.taobao.com/doc/detail.htm?id=118
    * ThisIsMyJam_ OAuth1 https://www.thisismyjam.com/developers/authentication
    * Trello_ OAuth1 https://trello.com/docs/gettingstarted/oauth.html
    * Tripit_ OAuth1
    * Tumblr_ OAuth1
    * Twilio_ Auth
    * Twitter_ OAuth1
    * VK.com_ OpenAPI, OAuth2 and OAuth2 for Applications
    * Weibo_ OAuth2
    * Xing_ OAuth1
    * Yahoo_ OpenId and OAuth1
    * Yammer_ OAuth2
    * Yandex_ OAuth1, OAuth2 and OpenId


User data
---------

Basic user data population, to allow custom field values from provider's
response.


Social accounts association
---------------------------

Multiple social accounts can be associated to a single user.


Authentication processing
-------------------------

Extensible pipeline to handle authentication/association mechanism in ways that
suits your project.


Dependencies
============

Dependencies that **must** be met to use the application:

- OpenId_ support depends on python-openid_

- OAuth_ support depends on python-oauth2_ (despite the name, this is just for
  OAuth1)

- Several backends demand application registration on their corresponding
  sites and other dependencies like sqlalchemy_ on Flask and Webpy.

- Other dependencies:
    * six_
    * requests_


Documents
=========

Project homepage is available at http://psa.matiasaguirre.net/ and documents at
http://psa.matiasaguirre.net or http://python-social-auth.readthedocs.org/.


Installation
============

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

Support
---------------------

If you're having problems with using the project, use the support forum at CodersClan.

.. image:: http://www.codersclan.net/graphics/getSupport_github4.png
    :target: http://codersclan.net/forum/index.php?repo_id=8


Copyrights and License
======================

``python-social-auth`` is protected by BSD license. Check the LICENSE_ for
details.

The base work was derived from django-social-auth_ work and copyrighted too,
check `django-social-auth LICENSE`_ for details:

.. _LICENSE: https://github.com/omab/python-social-auth/blob/master/LICENSE
.. _django-social-auth: https://github.com/omab/django-social-auth
.. _django-social-auth LICENSE: https://github.com/omab/django-social-auth/blob/master/LICENSE
.. _OpenId: http://openid.net/
.. _OAuth: http://oauth.net/
.. _myOpenID: https://www.myopenid.com/
.. _Angel: https://angel.co
.. _Appsfuel: http://docs.appsfuel.com
.. _Behance: https://www.behance.net
.. _Bitbucket: https://bitbucket.org
.. _Box: https://www.box.com
.. _Clef: https://getclef.com/
.. _Dailymotion: https://dailymotion.com
.. _Disqus: https://disqus.com
.. _Douban: http://www.douban.com
.. _Dropbox: https://dropbox.com
.. _Evernote: https://www.evernote.com
.. _Facebook: https://www.facebook.com
.. _Fitbit: https://fitbit.com
.. _Flickr: http://www.flickr.com
.. _Foursquare: https://foursquare.com
.. _Google App Engine: https://developers.google.com/appengine/
.. _Github: https://github.com
.. _Google: http://google.com
.. _Instagram: https://instagram.com
.. _Linkedin: https://www.linkedin.com
.. _Live: https://live.com
.. _Livejournal: http://livejournal.com
.. _Mailru: https://mail.ru
.. _Mixcloud: https://www.mixcloud.com
.. _Mozilla Persona: http://www.mozilla.org/persona/
.. _Odnoklassniki: http://www.odnoklassniki.ru
.. _Orkut: http://www.orkut.com
.. _Pocket: http://getpocket.com
.. _Podio: https://podio.com
.. _Shopify: http://shopify.com
.. _Skyrock: https://skyrock.com
.. _Soundcloud: https://soundcloud.com
.. _Stocktwits: https://stocktwits.com
.. _Stripe: https://stripe.com
.. _Taobao: http://open.taobao.com/doc/detail.htm?id=118
.. _Tripit: https://www.tripit.com
.. _Twilio: https://www.twilio.com
.. _Twitter: http://twitter.com
.. _VK.com: http://vk.com
.. _Weibo: https://weibo.com
.. _Xing: https://www.xing.com
.. _Yahoo: http://yahoo.com
.. _Yammer: https://www.yammer.com
.. _Yandex: https://yandex.ru
.. _Readability: http://www.readability.com/
.. _Stackoverflow: http://stackoverflow.com/
.. _Steam: http://steamcommunity.com/
.. _Rdio: https://www.rdio.com
.. _Tumblr: http://www.tumblr.com/
.. _Amazon: http://login.amazon.com/website
.. _AOL: http://www.aol.com/
.. _BelgiumEIDOpenId: https://www.e-contract.be/
.. _Fedora: http://fedoraproject.org/wiki/OpenID
.. _Jawbone: https://jawbone.com/up/developer/authentication
.. _Mendeley: http://mendeley.com
.. _Reddit: https://github.com/reddit/reddit/wiki/OAuth2
.. _OpenSuse: http://en.opensuse.org/openSUSE:Connect
.. _ThisIsMyJam: https://www.thisismyjam.com/developers/authentication
.. _Trello: https://trello.com/docs/gettingstarted/oauth.html
.. _Django: https://github.com/omab/python-social-auth/tree/master/social/apps/django_app
.. _Flask: https://github.com/omab/python-social-auth/tree/master/social/apps/flask_app
.. _Pyramid: http://www.pylonsproject.org/projects/pyramid/about
.. _Webpy: https://github.com/omab/python-social-auth/tree/master/social/apps/webpy_app
.. _Tornado: http://www.tornadoweb.org/
.. _python-openid: http://pypi.python.org/pypi/python-openid/
.. _python-oauth2: https://github.com/simplegeo/python-oauth2
.. _sqlalchemy: http://www.sqlalchemy.org/
.. _pypi: http://pypi.python.org/pypi/python-social-auth/
.. _OpenStreetMap: http://www.openstreetmap.org
.. _six: http://pythonhosted.org/six/
.. _requests: http://docs.python-requests.org/en/latest/
.. _PixelPin: http://pixelpin.co.uk
