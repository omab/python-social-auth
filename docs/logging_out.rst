Logging Out
===========

It's a common misconception that ``disconnect`` action is the same as logging
the user out, but is far from it.

``Disconnect`` is the way that your users have to say to you "forget about my
account", that implies removing the ``UserSocialAuth`` instance that was
created, this also implies that the user won't be able to login back into your
site with the social account, instead the action will be a signup, a new user
instance will be created, not related to the previous one.

Logging out is just a way to say "forget my current session", and usually
implies removing cookies, invalidating a session hash, etc. The many frameworks
have their own ways to logout an account (Django has ``django.contrib.auth.logout``),
``flask-login`` has it's own way too with `logout_user()`_.

Since disconnecting a social account means that the user won't be able to log
back in with that social provider into the same user, python-social-auth will
check that the user account is in a valid state for disconnection (it has at
least one more social account associated, or a password, etc). This behavior
can be overridden by changing the `Disconnection Pipeline`_.

.. _logout_user(): https://github.com/maxcountryman/flask-login/blob/a96de342eae560deec008a02179f593c3799b3ba/flask_login.py#L718-L739
.. _DISCONNECT_PIPELINE: pipeline.html#disconnection-pipeline
