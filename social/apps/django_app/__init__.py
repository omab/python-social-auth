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
