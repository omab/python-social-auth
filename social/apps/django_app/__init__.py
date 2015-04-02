"""
Django framework support.

To use this:
  * Add 'social.apps.django_app.default' if using default ORM,
    or 'social.apps.django_app.me' if using mongoengine
  * Add url('', include('social.apps.django_app.urls', namespace='social')) to
    urls.py
  * Define SOCIAL_AUTH_STORAGE and SOCIAL_AUTH_STRATEGY, default values:
    SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
    SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
"""
import django


if django.VERSION[0] == 1 and django.VERSION[1] < 7:
    from social.strategies.utils import set_current_strategy_getter
    from social.apps.django_app.utils import load_strategy
    # Set strategy loader method to workaround current strategy getter needed on
    # get_user() method on authentication backends when working with Django
    set_current_strategy_getter(load_strategy)
