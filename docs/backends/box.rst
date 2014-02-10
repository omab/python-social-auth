Box.net
=======

Box works similar to Facebook (OAuth2).

- Register an application at `Manage Box Applications`_

- Fill the **Consumer Key** and **Consumer Secret** values in your settings::

    SOCIAL_AUTH_BOX_KEY = ''
    SOCIAL_AUTH_BOX_SECRET = ''

- By default the token is not permanent, it will last an hour. To refresh the
  access token just do::

    from social.apps.django_app.utils import load_strategy

    strategy = load_strategy(backend='box')
    user = User.objects.get(pk=foo)
    social = user.social_auth.filter(provider='box')[0]
    social.refresh_token(strategy=strategy)

.. _Manage Box Applications: https://app.box.com/developers/services
