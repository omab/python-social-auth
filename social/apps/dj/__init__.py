"""
Django framework support.

To use this:
    * Add 'social.apps.dj.default' if using default ORM,
      or 'social.apps.dj.me' if using mongoengine
    * Add url('', 'social.apps.dj.urls') to urls.py
    * Define SOCIAL_AUTH_STORAGE and SOCIAL_AUTH_STRATEGY, default values:
        SOCIAL_AUTH_STRATEGY = 'social.strategies.dj.DjangoStrategy'
        SOCIAL_AUTH_STORAGE = 'social.apps.dj.default.models.DjangoStorage'
"""
