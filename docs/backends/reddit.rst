Reddit
======

Reddit implements `OAuth2 authentication workflow`_. To enable it, just follow:

- Register an application at `Reddit Preferences Apps`_

- Fill the **Consumer Key** and **Consumer Secret** values in your settings::

    SOCIAL_AUTH_REDDIT_KEY = ''
    SOCIAL_AUTH_REDDIT_SECRET = ''

- By default the token is not permanent, it will last an hour. To get
  a refresh token just define::

    SOCIAL_AUTH_REDDIT_AUTH_EXTRA_ARGUMENTS = {'duration': 'permanent'}

  This will store the ``refresh_token`` in ``UserSocialAuth.extra_data``
  attribute, to refresh the access token just do::

    from social.apps.django_app.utils import load_strategy

    strategy = load_strategy(backend='reddit')
    user = User.objects.get(pk=foo)
    social = user.social_auth.filter(provider='reddit')[0]
    social.refresh_token(strategy=strategy,
                         redirect_uri='http://localhost:8000/complete/reddit/')

  Reddit requires ``redirect_uri`` when refreshing the token and it must be the
  same value used during the auth process.

.. _Reddit Preferences Apps: https://ssl.reddit.com/prefs/apps/
.. _OAuth2 authentication workflow: https://github.com/reddit/reddit/wiki/OAuth2
